import os
from rq import Queue
from sqlalchemy import Enum
from lodjers import create_redis_connection
from lodjers.database import db
from lodjers.mail import welcome_notification, new_matches_notification

from datetime import datetime, timedelta

START_DATE_RANGE_MAX = 30   # days
MAX_EMAIL_FREQUENCY = 7     # days

conn = create_redis_connection(os.environ.get("APP_CONFIG_FILE") or "development")
q = Queue(connection=conn)

class User(db.Model):
    netid = db.Column(db.String(15), primary_key=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    joined_at = db.Column(db.DateTime)
    gender = db.Column(db.String(1))

    city = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    time_period = db.Column(db.SmallInteger)
    grad_year = db.Column(db.SmallInteger)
    searching = db.Column(db.Boolean)

    email_updates = db.Column(db.Boolean)
    last_visited = db.Column(db.DateTime)
    last_emailed = db.Column(db.DateTime)


    def __init__(self, full_name, netid, grad_year=None, city=None,
                 email_updates=True, searching=True, start_date=None,
                 time_period=3, last_emailed=None, gender=None):
        self.full_name = full_name
        self.nickname = full_name
        self.netid = netid
        self.gender = gender
        self.grad_year = grad_year
        self.start_date = start_date
        self.city = city
        self.time_period = time_period
        self.searching = searching
        self.email_updates = email_updates
        self.joined_at = datetime.now()
        self.last_visited = datetime.min
        self.last_emailed = last_emailed if last_emailed else \
                            datetime.now() - timedelta(days=MAX_EMAIL_FREQUENCY / 2)

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

    @property
    def email(self):
        if not self.grad_year:
            return self.netid + "@dartmouth.edu"

        split_name = map(lambda x: x.strip('.'), self.full_name.split())
        join_name = ".".join(split_name) + '.' + str(self.grad_year % 2000)
        return join_name + "@dartmouth.edu"

    def get_matches(self, for_email=False):
        if not self.start_date or not self.city:
            return []

        earliest_date = self.start_date - timedelta(days=START_DATE_RANGE_MAX)
        latest_date = self.start_date + timedelta(days=START_DATE_RANGE_MAX)

        matched_users = User.query.filter(User.city == self.city)   \
                                  .filter(User.netid != self.netid) \
                                  .filter(User.start_date
                                              .between(earliest_date,
                                                       latest_date))

        if for_email:
            matched_users = matched_users.filter(User.searching)             \
                                         .filter(User.gender == self.gender) \
                                         .filter(User.last_emailed <= datetime.now() - timedelta(days=MAX_EMAIL_FREQUENCY))

        return matched_users.all()

    def send_welcome_notification(self):
        q.enqueue(welcome_notification, self)

    def send_new_matches_notifications(self):
        for new_match in self.get_matches(for_email=True):
            q.enqueue(new_matches_notification, self, new_match)
            new_match.last_emailed = datetime.now()
            db.session.commit()

    def __repr__(self):
        return "%s (%s) - %s" % (self.full_name, self.netid, self.city)
