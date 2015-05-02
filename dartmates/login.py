# Adapted from Dartmouth Hacker Club

from flask import Blueprint, request, redirect, session, url_for
from flask.ext.login import LoginManager, login_user
import urllib
import requests
from lxml import etree

from dartmates.database import db
from dartmates.models import User

flask_cas = Blueprint('flask_cas', __name__, template_folder='templates')

CAS_URL = 'https://login.dartmouth.edu/cas/'
login_manager = LoginManager()


def recursive_dict(element):
    return element.tag, dict(map(recursive_dict, element)) or element.text


def cas_login(service):
    login_url = CAS_URL + 'login?' + urllib.urlencode(locals())
    return redirect(login_url)


def cas_validate(ticket, service):
    validate_url = CAS_URL + 'serviceValidate?' + urllib.urlencode(locals())
    r = requests.get(validate_url)
    doc = etree.fromstring(r.text)
    if 'authenticationSuccess' in doc[0].tag:
        return dict((key.replace('{http://www.yale.edu/tp/cas}', ''), value)
                    for key, value in recursive_dict(doc[0])[1].items())
    return None


@flask_cas.route("/login")
def login():
    callback_url = request.url.split('?')[0]
    if 'ticket' in request.args:
        user_data = cas_validate(request.args['ticket'], callback_url)
        user = User.query.filter_by(netid=user_data['netid']).first()
        if user is None:
            user = User(user_data['name'], user_data['netid'])
            db.session.add(user)
            db.session.commit()
        login_user(user)
    else:
        return cas_login(callback_url)

    return redirect(url_for('frontend.index'))


@flask_cas.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("frontend.index"))
