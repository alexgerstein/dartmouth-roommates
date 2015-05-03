from flask.ext.restful import Resource, fields, marshal
from flask.ext.login import login_required, current_user, logout_user

from dartmates.database import db

user_fields = {
    'full_name': fields.String,
    'nickname': fields.String,
    'city': fields.String,
    'number_of_roommates': fields.Integer,
    'start_date': fields.String,
    'time_period': fields.Integer
}


class UserAPI(Resource):
    @login_required
    def delete(self):
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return {'result': True}


class UserMatchesListAPI(Resource):
    @login_required
    def get(self):
        matches = current_user.get_roommate_matches()
        return {'users': [marshal(user, user_fields) for user in matches]}
