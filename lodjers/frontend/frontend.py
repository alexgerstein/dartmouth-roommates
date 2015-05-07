from . import bp
from flask import render_template
from flask.ext.login import login_required


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("index.html")


@bp.route('/profile')
@login_required
def profile():
    return render_template("profile.html")
