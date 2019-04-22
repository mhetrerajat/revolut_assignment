from flask_restful import Resource, reqparse, marshal, fields
from flask.json import jsonify
from app import auth, db
from flask import make_response
from app.models import Deposit, User

deposit_schema = {
    'currency': fields.String,
    'city': fields.String,
    'country': fields.String,
    'amount': fields.Float
}


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

        data = [marshal(deposit, deposit_schema) for deposit in data]

        return make_response(
            jsonify({
                'data': data,
                'message': None,
                'status': 'success'
            }))

    def post(self):
        args = self.reqparse.parse_args()

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

        return make_response(
            jsonify({
                'data': deposit_item,
                'message': 'Deposited!',
                'status': 'success'
            }))
