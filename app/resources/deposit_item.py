from flask import make_response
from flask.json import jsonify
from flask_restful import Resource, marshal, reqparse

from app import auth, db
from app.exceptions import ApiException
from app.models import Deposit, User
from app.utils.schema import DepositSchema


class DepositItem(Resource):
    decorators = [auth.login_required]

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('country',
                                   type=str,
                                   required=False,
                                   location="json")
        self.reqparse.add_argument('currency',
                                   type=str,
                                   required=False,
                                   location="json")
        self.reqparse.add_argument('amount',
                                   type=float,
                                   required=False,
                                   location="json")
        self.reqparse.add_argument('city',
                                   type=str,
                                   required=False,
                                   location="json")

        super(DepositItem, self).__init__()

    def get(self, deposit_id):
        user = User.query.filter_by(username=auth.username()).first()
        deposit = Deposit.query.filter_by(id=deposit_id,
                                          user=user.id).first_or_404()

        if not deposit:
            raise ApiException("Invalid deposit id.")

        return jsonify({
            'data': marshal(deposit, DepositSchema),
            'message': None,
            'status': 'success'
        })

    def put(self, deposit_id):
        args = self.reqparse.parse_args(strict=True)

        user = User.query.filter_by(username=auth.username()).first()
        deposit = Deposit.query.filter_by(id=deposit_id, user=user.id)

        if not deposit:
            raise ApiException("Invalid deposit id")

        update_values = {k: v for k, v in args.items() if v}
        deposit.update(update_values)

        db.session.commit()

        updated_deposit = Deposit.query.filter_by(id=deposit_id,
                                                  user=user.id).first()

        return make_response(
            jsonify({
                'data': marshal(updated_deposit, DepositSchema),
                'message': None,
                'status': 'success'
            }))

    def delete(self, deposit_id):
        user = User.query.filter_by(username=auth.username()).first()
        deposit = Deposit.query.filter_by(id=deposit_id, user=user.id).first()

        if not deposit:
            raise ApiException("Invalid deposit id")

        db.session.delete(deposit)
        db.session.commit()

        return jsonify({
            'data':
            None,
            'message':
            "Deleted deposit with id : {0}".format(deposit_id),
            'status':
            'success'
        })
