import json

from app import create_app, db
from app.models import User
from tests.base import BaseTestCase

from .context import app


def register_user(self, username, password):
    return self.client.post('/api/v1/auth/register',
                            data=json.dumps({
                                'username': username,
                                'password': password
                            }),
                            content_type='application/json')


class AuthResourcesTestCase(BaseTestCase):
    def test_registration(self):
        response = register_user(self, 'admin', 'admin')
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(data.get('data', {}).get('username'), 'admin')

    def test_register_duplicate_user(self):
        user = User(username='admin', password='admin')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = register_user(self, 'admin', 'admin')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('status'), 'failed')

    def test_missing_params(self):
        with self.client:
            response = register_user(self, None, 'admin')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertEqual(data.get('status'), 'failed')
