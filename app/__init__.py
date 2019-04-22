from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.exceptions import ApiException
from config import config

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

    api = Api(app, prefix="/api/v1")
    auth_api = Api(app, prefix='/api/v1/auth')
    deposit_api = Api(app, prefix='/api/v1/deposit')

    from app.resources.hello import Hello

    api.add_resource(Hello, '/')

    # Auth Resources
    from app.resources.register import Register
    auth_api.add_resource(Register, '/register')

    from app.resources.login import Login
    auth_api.add_resource(Login, '/login')

    # Deposit Resources
    from app.resources.nest_api import Nest
    deposit_api.add_resource(Nest, '/nest')

    from app.resources.deposit_item import DepositItem
    deposit_api.add_resource(DepositItem, '/<int:deposit_id>')

    from app.resources.deposit_list import DepositList
    deposit_api.add_resource(DepositList, '/')

    # Error Handler
    @app.errorhandler(ApiException)
    def handle_api_error(error):
        return error.get_response()

    return app
