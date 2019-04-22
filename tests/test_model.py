from passlib.apps import custom_app_context as pwd_context

from app import db, create_app
from app.models import User, Deposit
from tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError

from .context import app


class UserModelTestCases(BaseTestCase):
    def test_password_hashing(self):
        user = User(username='admin', password='admin')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(User.verify_password('admin', 'admin'))


class DepositModelTestCases(BaseTestCase):
    def test_insert_without_user(self):
        data = {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        }
        with self.assertRaises(IntegrityError):
            deposit = Deposit(**data)
            db.session.add(deposit)
            db.session.commit()
