from datetime import datetime
from flask.ext.restful import Resource, inputs, fields, marshal, reqparse
from flask.ext.login import login_required, current_user, logout_user

from dartmates.database import db

user_fields = {
    'netid': fields.String,
    'full_name': fields.String,
    'nickname': fields.String,
    'city': fields.String,
    'number_of_roommates': fields.Integer,
    'start_date': fields.String,
    'time_period': fields.Integer,
    'searching': fields.Boolean,
    'joined_at': fields.DateTime
}


class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('nickname', type=str)
        self.reqparse.add_argument('city', type=str, required=True)
        self.reqparse.add_argument('grad_year', type=int)
        self.reqparse.add_argument('start_date',
                                   type=str,
                                   required=True)
        self.reqparse.add_argument('time_period', type=int)
        self.reqparse.add_argument('number_of_roommates', type=str)
        self.reqparse.add_argument('searching', type=inputs.boolean)
        super(UserAPI, self).__init__()

    @login_required
    def get(self):
        return {'user': marshal(current_user, user_fields)}

    @login_required
    def put(self):
        args = self.reqparse.parse_args()

        for k, v in args.iteritems():
            if k == 'start_date':
                v = v.split('T')[0]
                v = datetime.strptime(v, "%Y-%m-%d")
            setattr(current_user, k, v)
        db.session.commit()

        return {'user': marshal(current_user, user_fields)}

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
