import unittest

from .context import app
from app.utils.parser import Parser


class ParserTestCase(unittest.TestCase):
    def setUp(self):
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
        self.parser = Parser(self.data, self.nesting_levels)

    def test_valid_parse(self):
        output = self.parser.parse()
        expected_output = {
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
        self.assertEqual(output, expected_output)

    def test_invalid_nesting_levels(self):
        invalid_levels = ['city', 'a']
        with self.assertRaises(ValueError):
            Parser(self.data, invalid_levels)
