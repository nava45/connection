from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, oid, db, login_manager
from app.users.forms import LoginForm
from datetime import datetime
from app.users.models import User, ROLE_USER, ROLE_ADMIN
from app.main_app.models import UserDetails
from app.decorators import crossdomain


users = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.login_form = LoginForm()
        #g.search_form = SearchForm()
 
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login_view'))
    user = User.query.filter_by(email = resp.email).first()
    userdetails = UserDetails(user=user)
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        
        db.session.add(user)
        db.session.add(userdetails)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
        
    userdetails = UserDetails.query.filter_by(user=user).first()
    if userdetails is None:
        userdetails = UserDetails(user=user)
        db.session.add(userdetails)
        db.session.commit()
        
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = True)
    return redirect(request.args.get('next') or url_for('main_flow.index'))


@users.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login_view():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('main_flow.index'))
    form = LoginForm()
    openid = request.form.get('openid',None)
    if form.validate_on_submit():
        print "logging"
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email','country','fullname','dob'])
    
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


@users.route('/profile/<nickname>', methods = ['GET', 'POST'])
def user_profile(nickname=None):
    if nickname is None:
        user = g.user
    else:
        user = User.query.filter_by(nickname=nickname).first()
    if user and user.is_authenticated():
        return render_template('user_profile.html',user=user)
    flash("The userprofile is not existing.")
    return render_template('user_profile.html')


@users.route('/ajax_login', methods = ['GET', 'POST'])  
def ajax_login():
    print "Ajax request", request.form.get('openid',None),request.form.get('provider',None)
    return jsonify({'d':1})

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_flow.index'))
