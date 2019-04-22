from flask import abort, make_response
from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import db
from app.exceptions import ApiException
from app.models import User


class Login(Resource):
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

        super(Login, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        user = User.query.filter_by(username=args.username).first()

        if not user or not user.verify_password(args.password):
            raise ApiException("Invalid username or password.")

        auth_token = user.encode_auth_token(user.id)

        response = {
            'data': auth_token.decode('utf-8'),
            'message': None,
            'status': 'success'
        }

        return make_response(jsonify(response))
