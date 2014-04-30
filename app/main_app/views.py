from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.admin.contrib import sqla

from sqlalchemy.sql.expression import func

from app.main_app.models import Category, Connection, ImageCategory, UserDetails
from app import db
#admin.add_view(sqla.ModelView(Category, db.session))


mf = Blueprint('main_flow', __name__)


@mf.route('/', methods = ['GET', 'POST'])
@mf.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page=1):
    """
    Index page of the web app
    """
    print request.method, g.user.nickname
    ud = UserDetails.query.filter_by(user=g.user).first()
    #connection = Connection.query.order_by(func.rand()).first()
    #connection = Connection.query.filter(Connection.id.notin_([i.id for i in ud.played_connections])).first()
    connection = Connection.query.intersect(ud.played_connections).first()
    if connection is None:
        return "yet connections to be added."
    
    IMAGES_PER_PAGE = 1
    
    if request.method == 'GET':
        image_sets = connection.embedded_images
        print "IS--::",image_sets,image_sets.count()
        TOTAL = image_sets.count()
        posts = image_sets.paginate(page, IMAGES_PER_PAGE, False)
        return render_template('index.html', posts=posts, total=TOTAL, page=page)
    else:
        print "answering", request.values.get('answering')
        ans = request.values.get('answering')
        if ans == connection.answer:
            ud.played_connections.append(connection)
            db.session.commit()
            return "success"
        
        image_sets = connection.embedded_images
        TOTAL = image_sets.count()
        posts = image_sets.paginate(page, IMAGES_PER_PAGE, False)
        return render_template('index.html', posts=posts, total=TOTAL, page=page)