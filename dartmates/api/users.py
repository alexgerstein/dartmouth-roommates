from flask.ext.restful import Resource
from flask.ext.login import current_user, logout_user

from dartmates.login import login_required
from dartmates.database import db


class UserAPI(Resource):
    @login_required
    def delete(self):
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return {'result': True}
