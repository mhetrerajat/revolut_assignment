import json

from app import create_app, db
from app.models import Deposit, User
from tests.base import BaseTestCase
from tests.base_deposit import (BaseDepositResourceTestCase,
                                get_basic_auth_token)
from tests.test_auth import register_user

from .context import app


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


class DepositListTestCases(BaseDepositResourceTestCase):
    def _insert_data(self):
        """
            This method insert data into database with Deposit POST API
        """
        for item in self.data:
            make_deposit_list_post_api_request(self, self.username,
                                               self.password, item)

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
