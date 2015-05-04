import os
import logging

DEBUG = True
SQLALCHEMY_ECHO = True

SECURITY_CONFIRMABLE = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_NATIVE_UNICODE = False

SECRET_KEY = os.environ['SECRET_KEY']

logger = logging.getLogger('lodjers')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

logger.info("Staging settings loaded.")
