from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response

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

    from app.resources.hello import Hello

    api.add_resource(Hello, '/')

    from app.resources.register import Register
    api.add_resource(Register, '/register')

    from app.resources.deposit_list import DepositList
    api.add_resource(DepositList, '/deposit')

    with app.app_context():
        db.create_all()

    return app
