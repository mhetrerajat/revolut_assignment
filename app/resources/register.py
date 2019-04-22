from flask import abort, make_response
from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import db
from app.exceptions import ApiException, UserAlreadyExistsException, RequirementParameterMissing
from app.models import User


class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   type=str,
                                   required=True,
                                   location="json",
                                   help="username cannot be blank!")
        self.reqparse.add_argument('password',
                                   type=str,
                                   required=True,
                                   location="json",
                                   help="password cannot be blank!")

        super(Register, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        if any([not args.username, not args.password]):
            raise RequirementParameterMissing(args)

        user = User.query.filter_by(username=args.username).first()
        if user:
            raise UserAlreadyExistsException(args.username)

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
