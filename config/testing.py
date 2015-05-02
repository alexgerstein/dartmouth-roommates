import os
import logging

basedir = os.path.abspath(os.path.dirname('manage.py'))

TESTING = True
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = ('sqlite:///:memory:')

logger = logging.getLogger('DARTmates')
logger.info("Testing settings loaded.")
