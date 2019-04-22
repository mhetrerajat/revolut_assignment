from flask_restful import fields


class DepositCurrencyField(fields.Raw):
    def format(self, value):
        return value.name
