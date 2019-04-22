import json

from app import create_app, db
from app.models import Deposit, User
from tests.base import BaseTestCase
from tests.test_auth import register_user

import base64

from .context import app


def get_basic_auth_token(username, password):
    return 'Basic ' + base64.b64encode(
        bytes("{0}:{1}".format(username, password), 'ascii')).decode('ascii')


def make_nest_api_request(self, username, password, data, nesting_levels):
    return self.client.post(
        '/api/v1/deposit/nest',
        data=json.dumps({
            'data': data,
            'nesting_levels': nesting_levels
        }),
        headers={'Authorization': get_basic_auth_token(username, password)}
        if username and password else {},
        content_type='application/json')


def make_deposit_list_post_api_request(self, username, password, data):
    return self.client.post(
        '/api/v1/deposit/',
        data=json.dumps(data),
        headers={'Authorization': get_basic_auth_token(username, password)}
        if username and password else {},
        content_type='application/json')


def make_deposit_list_get_api_request(self, username, password):
    return self.client.get(
        '/api/v1/deposit/',
        headers={'Authorization': get_basic_auth_token(username, password)}
        if username and password else {},
        content_type='application/json')


class DepositResourcesTestCases(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(DepositResourcesTestCases, self).__init__(*args, **kwargs)
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

    def _insert_data(self):
        """
            This method insert data into database with Deposit POST API
        """
        for item in self.data:
            make_deposit_list_post_api_request(self, self.username,
                                               self.password, item)

    def test_nest_api(self):
        """
            Valid request to Nest API
        """
        with self.client:

            # Create user for auth
            register_user(self, self.username, self.password)

            # Call Nest Api
            response = make_nest_api_request(self, self.username,
                                             self.password, self.data,
                                             self.nesting_levels)
            data = json.loads(response.data.decode())

            self.assertEqual(data.get('status'), 'success')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data.get('data', {}), self.expected_response)

    def test_nest_api_unauthorized_request(self):
        """
            Unauthorized request to Nest API
        """
        with self.client:
            response = make_nest_api_request(self, None, None, self.data,
                                             self.nesting_levels)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Unauthorized access')
            self.assertEqual(response.status_code, 401)

    def test_nest_api_missing_input(self):
        """
            One of the input is missing in request, here 'data' is empty.
        """
        # Create user for auth
        register_user(self, self.username, self.password)

        # Call Nest Api
        response = make_nest_api_request(self, self.username, self.password,
                                         [], self.nesting_levels)
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(response.status_code, 400)

    def test_nest_api_invalid_input(self):
        """
            One of the input has invalid value, here 'nesting_levels' has invalid
            level name. Level 'a' does not exists in actual data.
        """
        # Create user for auth
        register_user(self, self.username, self.password)

        # Call Nest Api
        response = make_nest_api_request(self, self.username, self.password,
                                         self.data, ['a'])
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(response.status_code, 400)

    def test_deposit_list_post_request(self):
        """
            Insert's deposits in database with API
        """
        with self.client:
            register_user(self, self.username, self.password)

            response = make_deposit_list_post_api_request(
                self, self.username, self.password, self.data[0])

            data = json.loads(response.data.decode())

            self.assertEqual(data.get('status'), 'success')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data.get('message'), 'Deposited!')

    def test_deposit_list_post_unauthorized_request(self):
        """
            Unauthorized request to Deposit Insert API
        """
        with self.client:
            response = make_deposit_list_post_api_request(
                self, self.username, self.password, self.data[0])
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Unauthorized access')
            self.assertEqual(response.status_code, 401)

    def test_deposit_list_get_request(self):
        """
            Validates number of deposits done by the user and returned by the api
        """

        with self.client:
            register_user(self, self.username, self.password)

            self._insert_data()

            response = make_deposit_list_get_api_request(
                self, self.username, self.password)

            data = json.loads(response.data.decode())

            self.assertEqual(data.get('status'), 'success')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data.get('data', [])), len(self.data))

    def test_deposit_list_get_unauthorized_request(self):
        """
            Unauthorized request to Deposit List Fetch API
        """
        with self.client:
            response = make_deposit_list_get_api_request(
                self, self.username, self.password)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Unauthorized access')
            self.assertEqual(response.status_code, 401)