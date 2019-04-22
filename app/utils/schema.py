from flask_restful import fields

from app.models import DepositCurrency
from app.utils.fields import DepositCurrencyField

DepositSchema = {
    'currency': DepositCurrencyField,
    'city': fields.String,
    'country': fields.String,
    'amount': fields.Float
}
