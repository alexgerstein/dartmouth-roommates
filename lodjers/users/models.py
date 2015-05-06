from lodjers.database import db
from datetime import datetime, timedelta

START_DATE_RANGE_MAX = 30


class User(db.Model):
    netid = db.Column(db.String(15), primary_key=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    joined_at = db.Column(db.DateTime)

    city = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    time_period = db.Column(db.SmallInteger)
    grad_year = db.Column(db.SmallInteger)
    searching = db.Column(db.Boolean)

    email_updates = db.Column(db.Boolean)
    last_visited = db.Column(db.DateTime)

    def __init__(self, full_name, netid, grad_year=None, city=None,
                 email_updates=True, searching=True, start_date=None,
                 time_period=12):
        self.full_name = full_name
        self.nickname = full_name
        self.netid = netid
        self.grad_year = grad_year
        self.start_date = start_date
        self.city = city
        self.time_period = time_period
        self.searching = searching
        self.email_updates = email_updates
        self.joined_at = datetime.now()
        self.last_visited = datetime.min

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
        if not self.start_date or not self.city:
            return []

        earliest_date = self.start_date - timedelta(days=START_DATE_RANGE_MAX)
        latest_date = self.start_date + timedelta(days=START_DATE_RANGE_MAX)

        matched_users = User.query.filter(User.city == self.city)   \
                                  .filter(User.netid != self.netid) \
                                  .filter(User.start_date.between(earliest_date, latest_date))               \
                                  .filter(User.searching)           \
                                  .all()
        return matched_users
