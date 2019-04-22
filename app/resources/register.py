from flask import abort, make_response
from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import db
from app.exceptions import ApiException
from app.models import User


class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   type=str,
                                   required=True,
                                   location="json")
        self.reqparse.add_argument('password',
                                   type=str,
                                   required=True,
                                   location="json")

        super(Register, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        user = User.query.filter_by(username=args.username).first()
        if user:
            raise ApiException(
                "User {0} already exists. Please use different username.".
                format(args.username),
                status=401)

        user = User(args.username, args.password)
        db.session.add(user)
        db.session.commit()

        response = {
            'data': {
                'username': args.username
            },
            'message': "User created successfully!",
            'status': 'success'
        }

        return make_response(jsonify(response))
