import os
import logging

basedir = os.path.abspath(os.path.dirname('manage.py'))

DEBUG = False
CSRF_ENABLED = True
SECRET_KEY = 'youll-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_RECORD_QUERIES = True

logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger('DARTmates')
logger.setLevel(logging.INFO)

logger.info("Default settings loaded.")
