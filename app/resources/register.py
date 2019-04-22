from flask import abort
from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import db
from app.models import User


class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True)
        self.reqparse.add_argument('password', type=str, required=True)

        super(Register, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        user = User.query.filter_by(username=args.username).first()
        if user:
            abort(400)

        user = User(args.username, args.password)
        db.session.add(user)
        db.session.commit()

        return {'username': args.username, 'message': 'Account Created!'}
