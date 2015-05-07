import os
import sys
import subprocess
from datetime import datetime
from lodjers import create_app, create_redis_connection
from lodjers.database import db
from lodjers.models import User
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets
from rq import Worker, Queue, Connection

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
conn = create_redis_connection(os.environ.get("APP_CONFIG_FILE") or "development")
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
    for i in range(10):
        user = User(full_name="User %d" % i, netid="%d" % i,
                    city="san francisco", start_date=datetime.now(),
                    grad_year=2015)
        db.session.add(user)
        db.session.commit()


@manager.command
def worker():
    """
    Starts redis queue worker. Requires redis-server
    To run (in background): 'redis-server &'
    To kill: 'redis-cli shutdown'
    """
    listen = ['default']
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets)


if __name__ == '__main__':
    manager.run()
