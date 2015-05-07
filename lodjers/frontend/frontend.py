from . import bp
from flask import render_template
from flask.ext.security import login_required
from lodjers.models import User


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("index.html")


@bp.route('/profile')
@login_required
def profile():
    return render_template("profile.html")
