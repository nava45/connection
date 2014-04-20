from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g



mf = Blueprint('main_flow', __name__)


@mf.route('/')
def index():
    """
    Index page of the web app
    """
  
    return render_template('index.html')
