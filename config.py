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
    POST_PER_PAGE = 4
