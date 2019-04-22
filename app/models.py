from datetime import datetime, timedelta

from flask import current_app as app
from passlib.apps import custom_app_context as pwd_context

from app import db, auth


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
        return pwd_context.encrypt(password)

    @staticmethod
    @auth.verify_password
    def verify_password(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not pwd_context.verify(password, user.password):
            return False
        return True
