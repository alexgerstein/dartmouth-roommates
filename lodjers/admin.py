from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from lodjers.database import db
from lodjers.models import User

admin = Admin()


class UserView(ModelView):
    can_create = False
    can_delete = True

    def is_accessible(self):
        return current_user.is_authenticated() and \
               current_user.netid == "d36395d"

    column_display_pk = True
    form_columns = ['nickname', 'city']


admin.add_view(UserView(User, db.session))
