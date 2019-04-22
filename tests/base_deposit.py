import base64

from app import create_app, db
from app.models import Deposit, User
from tests.base import BaseTestCase
from tests.test_auth import register_user

from .context import app


def get_basic_auth_token(username, password):
    return 'Basic ' + base64.b64encode(
        bytes("{0}:{1}".format(username, password), 'ascii')).decode('ascii')


class BaseDepositResourceTestCase(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(BaseDepositResourceTestCase, self).__init__(*args, **kwargs)
        self.data = [{
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        }, {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        }, {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        }]
        self.nesting_levels = ['currency', 'country', 'city']
        self.username = "admin"
        self.password = "admin"
        self.expected_response = {
            'USD': {
                'US': {
                    'Boston': [{
                        'amount': 100
                    }]
                }
            },
            'EUR': {
                'FR': {
                    'Paris': [{
                        'amount': 20
                    }],
                    'Lyon': [{
                        'amount': 11.4
                    }]
                }
            }
        }
