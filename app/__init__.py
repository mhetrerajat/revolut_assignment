from flask import Flask
from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from app.resources.hello import Hello

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    api = Api(app)
    api.add_resource(Hello, '/')

    with app.app_context():
        db.create_all()

    return app