import os
from dotenv import load_dotenv

# Path to this file (config.py), that receives data from secret file '.env'
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(36) or 'to-long-pass-for-understanding'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATION = False
    POSTS_PER_PAGE = 5
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# Settings from Google -> help
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USR_SSL = True
