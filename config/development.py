import logging

DEBUG = True
SQLALCHEMY_ECHO = True

logger = logging.getLogger('DARTmates')
logger.setLevel(logging.DEBUG)

logger.info("Development settings loaded.")
