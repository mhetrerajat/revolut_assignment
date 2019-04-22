from flask.json import jsonify
from flask_restful import Resource, reqparse

from app import auth
from app.exceptions import ApiException
from app.utils.parser import Parser


class Nest(Resource):

    decorators = [auth.login_required]

    def __init__(self, *args, **kwargs):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data',
                                   type=list,
                                   required=True,
                                   location='json')
        self.reqparse.add_argument('nesting_levels',
                                   type=list,
                                   required=True,
                                   location='json')

        super(Nest, self).__init__(*args, **kwargs)

    def post(self):
        args = self.reqparse.parse_args()

        try:
            p = Parser(args.data, args.nesting_levels)
            output = p.parse()
            response = {'data': output, 'message': None, 'status': 'success'}
        except Exception as e:
            raise ApiException(str(e))

        return jsonify(response)
