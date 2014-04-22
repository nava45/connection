from flask.ext.admin import form
from flask.ext.admin.form import rules
from flask.ext.admin.contrib import sqla
from jinja2 import Markup
from flask import url_for
from app import db, app, admin
from config import _basedir
import os
import os.path as op

file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_played = db.Column(db.DateTime)
    high_score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return '<User Details %r - %r>' % (self.name, self.rank)
    
relevant_images = db.Table('relevant_images',
    db.Column('img', db.Integer, db.ForeignKey('image_category.id')),
    db.Column('connection', db.Integer, db.ForeignKey('connection.id'))
    )

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.Unicode(140), unique=True, index=True)
    embedded_images = db.relationship('ImageCategory', secondary=relevant_images,
        backref=db.backref('connections', lazy='dynamic'))
    hint = db.Column(db.Unicode(150), nullable=True)
    
    def __repr__(self):
        return '<Connection %r>' % (self.answer)
    
    
class ImageCategory(db.Model):
    __tablename__ = 'image_category'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Unicode(64), unique=True, index=True)
    path = db.Column(db.Unicode(128))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    hint = db.Column(db.Unicode(150), nullable=True)
    
    def __repr__(self):
        return '<Brainy %r>' % (self.name)
    
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True, index=True)
    
    
    def __repr__(self):
        return '<Category %r>' % (self.name)
    
    
class ImageView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))

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
    
admin.add_view(sqla.ModelView(Connection, db.session))
admin.add_view(sqla.ModelView(Category, db.session))
admin.add_view(ImageView(ImageCategory, db.session))