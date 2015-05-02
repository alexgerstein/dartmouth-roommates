from . import bp
from flask import render_template
from dartmates.models import User


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("index.html",
                           user_count=format(User.query.count(), ",d"))
