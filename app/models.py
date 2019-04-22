import enum
from datetime import datetime

from flask import current_app as app
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.types import Enum

from app import auth, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
        self.registered_on = datetime.utcnow()

    def hash_password(self, password):
        return pwd_context.hash(password)

    @staticmethod
    @auth.verify_password
    def verify_password(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not pwd_context.verify(password, user.password):
            return False
        return True


class DepositCurrency(enum.Enum):
    INR = 0
    EUR = 1
    USD = 2
    GBP = 3
    FBP = 4


class Deposit(db.Model):
    __tablename__ = 'deposits'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    currency = db.Column(Enum(DepositCurrency), nullable=False)
    user = db.Column(db.ForeignKey('users.id'), index=True, nullable=False)
    amount = db.Column(db.Float(asdecimal=True), nullable=False)
