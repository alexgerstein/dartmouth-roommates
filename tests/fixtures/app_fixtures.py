import pytest
from rq import SimpleWorker, Queue
from rq import push_connection, pop_connection

from lodjers import create_app, create_redis_connection
from lodjers.database import db as _db
from lodjers.mail import mail

from tests.factories import user_factories


@pytest.yield_fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application"""
    app = create_app("testing")

    # Establish an application context before running the tests.
    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app, request):
    """Session-wide test database"""

    _db.drop_all()
    _db.create_all()
    _db.app = app

    yield _db


@pytest.yield_fixture(autouse=True)
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    options = dict(bind=connection, expire_on_commit=False)
    session = db.create_scoped_session(options)
    db.session = session

    user_factories.UserFactory._meta.sqlalchemy_session = session
    user_factories.SanFranciscoUserFactory._meta.sqlalchemy_session = session

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture()
def test_client(app, request):
    with app.test_client() as client:
        yield client


@pytest.yield_fixture()
def connection(request):
    push_connection(create_redis_connection('testing'))
    yield
    pop_connection()


@pytest.yield_fixture()
def queue(connection, request):
    yield Queue()


@pytest.yield_fixture()
def worker(queue, request):
    yield SimpleWorker([queue])


@pytest.yield_fixture()
def outbox(request):
    with mail.record_messages() as outbox:
        yield outbox
