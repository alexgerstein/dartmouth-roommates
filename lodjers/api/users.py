from datetime import datetime
from flask.ext.restful import Resource, inputs, fields, marshal, reqparse
from flask.ext.login import login_required, current_user, logout_user

from lodjers.database import db

CITY_ABBREVIATIONS = {'nyc': 'new york city', 'ny': 'new york city', 'sf': "san francisco", 'la': 'los angeles', 'chi': 'chicago', 'n.y.c': 'new york city', 'washington dc': 'washington d.c.', 'd.c.': 'washington d.c.', 'dc': 'washington d.c.'}


class isNew(fields.Raw):
    def output(self, key, user):
        if not current_user.last_visited:
            return True

        return current_user.last_visited <= user.joined_at

user_fields = {
    'netid': fields.String,
    'full_name': fields.String,
    'nickname': fields.String,
    'grad_year': fields.Integer(default=None),
    'city': fields.String,
    'start_date': fields.String,
    'time_period': fields.Integer,
    'searching': fields.Boolean,
    'joined_at': fields.DateTime,
    'new': isNew
}


class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('nickname', type=str, required=True)
        self.reqparse.add_argument('city', type=str)
        self.reqparse.add_argument('grad_year', type=int, required=True)
        self.reqparse.add_argument('start_date', type=str, required=True)
        self.reqparse.add_argument('time_period', type=int, required=True)
        self.reqparse.add_argument('searching', type=inputs.boolean, required=True)
        super(UserAPI, self).__init__()

    @login_required
    def get(self):
        return {'user': marshal(current_user, user_fields)}

    @login_required
    def put(self):
        args = self.reqparse.parse_args()

        previously_searching = current_user.searching
        for k, v in args.iteritems():
            if k == 'start_date':
                if v:
                    v = v.split('T')[0]
                    v = datetime.strptime(v, "%Y-%m-%d")
            if k == 'city':
                if v:
                    v = v.lower()

                if v in CITY_ABBREVIATIONS:
                    v = CITY_ABBREVIATIONS[v]
            setattr(current_user, k, v)
        db.session.commit()

        if not previously_searching and current_user.searching:
            current_user.send_new_matches_notifications()

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
        data = {'users': [marshal(user, user_fields) for user in matches]}

        current_user.last_visited = datetime.now()
        db.session.commit()

        return data
