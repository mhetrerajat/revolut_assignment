import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'wJ6SOHBzXEnrZ5ZUYduZleR0kGrah5MTGMtytR9gUrg='
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SSL_REDIRECT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}
