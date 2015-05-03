from dartmates.database import db


class User(db.Model):
    netid = db.Column(db.String(15), primary_key=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))

    city = db.Column(db.String(200))
    number_of_roommates = db.Column(db.SmallInteger)
    start_date = db.Column(db.Date)
    time_period = db.Column(db.SmallInteger)
    searching = db.Column(db.Boolean)

    email_updates = db.Column(db.Boolean)

    def __init__(self, full_name, netid, grad_year=None, city=None, email_updates=True, searching=True, time_period=12, number_of_roommates=1, start_date=None):
        self.full_name = full_name
        self.nickname = full_name
        self.netid = netid
        self.grad_year = grad_year
        self.start_date = start_date
        self.city = city
        self.time_period = time_period
        self.number_of_roommates = number_of_roommates
        self.searching = searching
        self.email_updates = email_updates

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

    def get_roommate_matches(self):
        return []
