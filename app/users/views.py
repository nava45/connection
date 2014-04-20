from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from app.users.forms import LoginForm


users = Blueprint('users', __name__)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        #db.session.commit()
        #g.search_form = SearchForm()
 


@users.route('/login', methods = ['GET', 'POST'])
#oid.loginhandler
def login_view():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
