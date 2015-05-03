import os
import sys
import subprocess
from datetime import datetime
from dartmates import create_app
from dartmates.database import db
from dartmates.models import User
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db, 'User': User}


@manager.command
def tests():
    status = subprocess.call("bash ./scripts/test.sh", shell=True)
    sys.exit(status)


@manager.command
def seed():
    for i in range(5):
        user = User(full_name="User %d" % i, netid="%d" % i,
                    city="San Francisco", start_date=datetime.now(),
                    grad_year=2015)
        db.session.add(user)
        db.session.commit()


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
