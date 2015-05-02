from dartmates.database import db


class User(db.Model):
    netid = db.Column(db.String(15), primary_key=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))

    city = db.Column(db.String(200))
    number_of_roommates = db.Column(db.SmallInteger)
    start_date = db.Column(db.Date)
    time_period = db.Column(db.SmallInteger)
    grad_year = db.Column(db.SmallInteger)
    searching = db.Column(db.Boolean)

    email_updates = db.Column(db.Boolean)

    def __init__(self, full_name, netid):
        self.full_name = full_name
        self.netid = netid
        self.nickname = full_name
        self.searching = True
        self.email_updates = True

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.netid

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
