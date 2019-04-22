from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response

from config import config

from app.exceptions import ApiException

db = SQLAlchemy()
auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    @app.errorhandler(ApiException)
    def handle_api_error(error):
        return error.get_response()

    api = Api(app, prefix="/api/v1")

    from app.resources.hello import Hello

    api.add_resource(Hello, '/')

    from app.resources.register import Register
    api.add_resource(Register, '/register')

    from app.resources.login import Login
    api.add_resource(Login, '/login')

    from app.resources.deposit_item import DepositItem
    api.add_resource(DepositItem, '/deposit/<int:deposit_id>')

    from app.resources.nest_api import Nest
    api.add_resource(Nest, '/deposit/nest')

    from app.resources.deposit_list import DepositList
    api.add_resource(DepositList, '/deposit')

    return app
