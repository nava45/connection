import os

from flask import Flask, request, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.openid import OpenID
from flask.ext.mail import Mail
from flask.ext.admin import Admin

from config import _basedir

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app) 
db = SQLAlchemy(app)
mail = Mail(app)
admin = Admin(app)


login_manager.login_view = "users.login_view"
login_manager.login_message = "Log in da !"

oid = OpenID(app, os.path.join(_basedir, 'tmp'))

#debugtoolbar

if app.debug:
    from flask_debugtoolbar import DebugToolbarExtension
    from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
    
    toolbar = DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    app.config['DEBUG_TB_PANELS'] = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the line profiling
        'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel'
    ]
    

#BluePrint register
from app.users.views import users
app.register_blueprint(users)

#Main app module
from app.main_app.views import mf
app.register_blueprint(mf)

#Static files

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

"""
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
"""

@app.template_filter('capfirst')
def capfirst(s):
    #print s,type(s),dir(s),s.text
    return s.text.capitalize()

@app.template_filter('unique')
def unique(s):
    print "messages",s
    return set(s)
