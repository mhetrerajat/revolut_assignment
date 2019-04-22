from flask import make_response
from flask.json import jsonify
from flask_restful import Resource, fields, marshal, reqparse

from app import auth, db
from app.exceptions import RequirementParameterMissing
from app.models import Deposit, User
from app.utils.schema import DepositSchema


class DepositList(Resource):

    decorators = [auth.login_required]

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('country',
                                   type=str,
                                   required=True,
                                   location="json")
        self.reqparse.add_argument('currency',
                                   type=str,
                                   required=True,
                                   location="json")
        self.reqparse.add_argument('amount',
                                   type=float,
                                   required=True,
                                   location="json")
        self.reqparse.add_argument('city',
                                   type=str,
                                   required=True,
                                   location="json")

        super(DepositList, self).__init__()

    def get(self):

        user = User.query.filter_by(username=auth.username()).first()

        data = Deposit.query.filter_by(user=user.id)

        data = [marshal(deposit, DepositSchema) for deposit in data]

        return make_response(
            jsonify({
                'data': data,
                'message': None,
                'status': 'success'
            }))

    def post(self):
        args = self.reqparse.parse_args()

        # Make sure all parameters are present
        if any([not v for k, v in args.items()]):
            raise RequirementParameterMissing(args)

        user = User.query.filter_by(username=auth.username()).first()

        deposit_item = {
            'country': args.country,
            'city': args.city,
            'currency': args.currency,
            'amount': args.amount,
            'user': user.id
        }
        deposit = Deposit(**deposit_item)
        db.session.add(deposit)
        db.session.commit()

        deposit_item.update({'id': deposit.id})

        return make_response(
            jsonify({
                'data': deposit_item,
                'message': 'Deposited!',
                'status': 'success'
            }), 201)
