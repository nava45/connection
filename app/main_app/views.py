from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g

from flask.ext.login import login_user, logout_user, current_user, login_required


mf = Blueprint('main_flow', __name__)


@mf.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    """
    Index page of the web app
    """
    print "calll"
    print "request data", request.data,request.args
    return render_template('index.html')
