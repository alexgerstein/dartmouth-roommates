from flask import Blueprint
from flask.ext.restful import Api

from users import UserAPI, UserMatchesListAPI

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")

api.add_resource(UserAPI, '/user', endpoint='user')
api.add_resource(UserMatchesListAPI, '/users/matches', endpoint='matches')
