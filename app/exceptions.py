from flask import jsonify


class ApiException(Exception):
    def __init__(self, message, status=400, *args, **kwargs):
        self.message = message
        self.status = status

    def get_response(self):
        return jsonify({
            'data': None,
            'message': self.message,
            'status': 'failed'
        }), self.status
