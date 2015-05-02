from dartplan.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(15), index=True, unique=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    grad_year = db.Column(db.SmallInteger)

    email_updates = db.Column(db.Boolean)

    def __init__(self, full_name, netid):
        self.full_name = full_name
        self.netid = netid
        self.nickname = full_name
        self.email_updates = True
