import json

from app import create_app, db
from app.models import Deposit, User
from tests.base import BaseTestCase
from tests.base_deposit import (BaseDepositResourceTestCase,
                                get_basic_auth_token)
from tests.test_auth import register_user
from tests.test_deposit_list import make_deposit_list_post_api_request

from .context import app


def make_deposit_item_get_api_request(self, username, password, deposit_id):
    return self.client.get(
        '/api/v1/deposit/{0}'.format(deposit_id),
        headers={'Authorization': get_basic_auth_token(username, password)}
        if username and password else {},
        content_type='application/json')


def make_deposit_item_update_api_request(self, username, password, deposit_id,
                                         data):
    return self.client.put(
        '/api/v1/deposit/{0}'.format(deposit_id),
        data=json.dumps(data),
        headers={'Authorization': get_basic_auth_token(username, password)}
        if username and password else {},
        content_type='application/json')


def make_deposit_item_delete_api_request(self, username, password, deposit_id):
    return self.client.delete(
        '/api/v1/deposit/{0}'.format(deposit_id),
        headers={'Authorization': get_basic_auth_token(username, password)}
        if username and password else {},
        content_type='application/json')


class DepositItemTestCases(BaseDepositResourceTestCase):
    def test_deposit_item_get_api(self):

        with self.client:
            # Auth
            register_user(self, self.username, self.password)

            # Insert Deposit
            response = make_deposit_list_post_api_request(
                self, self.username, self.password, self.data[0])
            data = json.loads(response.data.decode())
            deposit_id = data.get('data', {}).get('id')

            self.assertIsNotNone(deposit_id)

            # Fetch deposit by id
            response = make_deposit_item_get_api_request(
                self, self.username, self.password, deposit_id)
            data = json.loads(response.data.decode())

            self.assertEqual(data.get('status'), 'success')
            self.assert200(response)
            self.assertEqual(data.get('data', {}).get('id'), deposit_id)

    def test_deposit_item_get_unauthorized_request(self):
        with self.client:
            response = make_deposit_item_get_api_request(
                self, self.username, self.password, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Unauthorized access')
            self.assertEqual(response.status_code, 401)

    def test_deposit_item_get_invalid_deposit_id(self):
        with self.client:
            # Auth
            register_user(self, self.username, self.password)

            # Deposit Item Get API
            response = make_deposit_item_get_api_request(
                self, self.username, self.password, "a")
            self.assert404(response)

    def test_deposit_item_update_api(self):
        # Auth
        register_user(self, self.username, self.password)

        # Insert Deposit
        response = make_deposit_list_post_api_request(self, self.username,
                                                      self.password,
                                                      self.data[0])
        data = json.loads(response.data.decode())
        deposit_id = data.get('data', {}).get('id')
        data.get('data', {}).get('amount')

        self.assertIsNotNone(deposit_id)

        # Update Amount
        response = make_deposit_item_update_api_request(
            self, self.username, self.password, deposit_id, {'amount': 1000})
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'success')
        self.assert200(response)
        self.assertEqual(data.get('data', {}).get('id'), deposit_id)

        self.assertEqual(data.get('data', {}).get('amount'), 1000)

    def test_deposit_item_update_invalid_deposit_id(self):
        with self.client:
            # Auth
            register_user(self, self.username, self.password)

            # Deposit Item Update API
            response = make_deposit_item_update_api_request(
                self, self.username, self.password, "a", {'amount': 1000})
            self.assert404(response)

    def test_deposit_item_update_unauthorized_request(self):
        with self.client:
            response = make_deposit_item_update_api_request(
                self, self.username, self.password, 1, {'amount': 1000})
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Unauthorized access')
            self.assertEqual(response.status_code, 401)

    def test_deposit_item_delete_api(self):
        # Auth
        register_user(self, self.username, self.password)

        # Insert Deposit
        response = make_deposit_list_post_api_request(self, self.username,
                                                      self.password,
                                                      self.data[0])
        data = json.loads(response.data.decode())
        deposit_id = data.get('data', {}).get('id')

        self.assertIsNotNone(deposit_id)

        # Delete deposit
        response = make_deposit_item_delete_api_request(
            self, self.username, self.password, deposit_id)
        data = json.loads(response.data.decode())

        message = data.get('message')
        expected_message = "Deleted deposit with id : {0}".format(deposit_id)

        self.assertEqual(message, expected_message)
        self.assert200(response)

    def test_deposit_item_delete_unauthorized_request(self):
        with self.client:
            response = make_deposit_item_delete_api_request(
                self, self.username, self.password, 1)
            data = json.loads(response.data.decode())
            self.assertEqual(data.get('message'), 'Unauthorized access')
            self.assertEqual(response.status_code, 401)

    def test_deposit_item_delete_invalid_deposit_id(self):
        with self.client:
            # Auth
            register_user(self, self.username, self.password)

            # Deposit Item Delete API
            response = make_deposit_item_delete_api_request(
                self, self.username, self.password, "a")
            self.assert404(response)
