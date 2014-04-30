from flask import redirect
from flask.ext import admin, login
from flask.ext.admin import helpers, expose
from flask.ext.admin import form
from flask.ext.admin.form import rules
from flask.ext.admin.contrib import sqla
from sqlalchemy.event import listens_for
from jinja2 import Markup
from flask import url_for
from app import db, app
from config import _basedir, file_path
import os

from app.users.models import User
file_path = os.path.join(app.static_folder, 'play_files')

connection_images = db.Table('connection_images',
    db.Column('img', db.Integer, db.ForeignKey('image_category.id')),
    db.Column('connection', db.Integer, db.ForeignKey('connection.id'))
    )


user_played = db.Table('user_played',
    db.Column('user', db.Integer, db.ForeignKey('user_details.id')),
    db.Column('played', db.Integer, db.ForeignKey('connection.id'))
    )

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_played = db.Column(db.DateTime, default=db.func.now())
    high_score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)
    played_connections = db.relationship('Connection',
                                         secondary=user_played,
                                         backref=db.backref('userdetails', lazy='dynamic'),lazy='dynamic')
    user = db.relationship('User',
                           primaryjoin='UserDetails.user_id == User.id', 
                           backref=db.backref('userdetails', lazy='dynamic')
                           )
    
    def __repr__(self):
        return '<User Details %r - %r>' % (self.user_id, self.rank)
    


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.Unicode(140), unique=True, index=True)
    embedded_images = db.relationship('ImageCategory', secondary=connection_images,
        backref=db.backref('connections', lazy='dynamic'), lazy='dynamic')
    hint = db.Column(db.Unicode(150), nullable=True)
    
    def __repr__(self):
        return '<Connection %r>' % (self.answer)
    
    
class ImageCategory(db.Model):
    __tablename__ = 'image_category'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Unicode(64), unique=True, index=True)
    path = db.Column(db.Unicode(128), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    hint = db.Column(db.Unicode(150), nullable=True)
    
    def __repr__(self):
        return '<Brainy %r>' % (self.name)
    
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True, index=True)
    
    
    def __repr__(self):
        return '<Category %r>' % (self.name)
    

class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('users.login_view'))
        return super(MyAdminIndexView, self).index()

class ImageView(sqla.ModelView):
    
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        print "admin",model.path
        return Markup('<img src="/static/play_files/%s">' % form.thumbgen_filename(model.path))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }

admin = admin.Admin(app, 'Auth', index_view=MyAdminIndexView())

admin.add_view(sqla.ModelView(Connection, db.session))
admin.add_view(sqla.ModelView(Category, db.session))
admin.add_view(ImageView(ImageCategory, db.session))
admin.add_view(sqla.ModelView(User, db.session))
admin.add_view(sqla.ModelView(UserDetails, db.session))


@listens_for(ImageCategory, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(os.path.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(os.path.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass