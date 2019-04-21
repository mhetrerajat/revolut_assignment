from flask_restful import Resource
from flask.json import jsonify


class Hello(Resource):
    def get(self):
        return jsonify({
            'data': None,
            'message': 'Hello! Revolut Data Engineer Assignment',
            'status': 'success'
        })