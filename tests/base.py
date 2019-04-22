from flask_testing import TestCase

from app import create_app as _create_app
from app import db

from .context import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = _create_app('test')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
