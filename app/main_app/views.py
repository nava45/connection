from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g

from flask.ext.login import login_user, logout_user, current_user, login_required


mf = Blueprint('main_flow', __name__)


@mf.route('/')
@login_required
def index():
    """
    Index page of the web app
    """
  
    return render_template('index.html')
