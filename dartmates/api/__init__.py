from flask import Blueprint
from flask.ext.restful import Api

from users import UserAPI

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")

api.add_resource(UserAPI, '/user', endpoint='user')
