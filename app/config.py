import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', None) or 'dev'
    MONGODB_URI = os.environ.get('MONGODB_URI', None)
