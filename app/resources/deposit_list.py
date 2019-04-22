from flask_restful import Resource
from flask.json import jsonify
from app import auth, db


class DepositList(Resource):

    decorators = [auth.login_required]

    def get(self):
        return jsonify({
            'data': None,
            'message': 'Get Deposit List',
            'status': 'success'
        })