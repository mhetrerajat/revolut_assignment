import json

from app import create_app, db
from app.models import Deposit, User
from tests.base import BaseTestCase
from tests.base_deposit import (BaseDepositResourceTestCase,
                                get_basic_auth_token)
from tests.test_auth import register_user

from .context import app


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


class NestApiTestCases(BaseDepositResourceTestCase):
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
