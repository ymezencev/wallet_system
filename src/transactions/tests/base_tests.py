from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APITestCase

from transactions.models import Reason
from wallets.models import Currency
from wallets.services.currency import update_currency_rates
from wallets.services.wallet import create_wallet


class BaseTestCase(APITestCase):
    """Тесты транзакций"""

    def setUp(self):

        self.client = Client()
        update_currency_rates()

        self.user_data = {'username': 'test_user',
                          'email': 'test_user@email.ru'}
        self.user = get_user_model()(**self.user_data)
        self.user.set_password('StrongPassword123')
        self.user.save()
        self.rub_currency = Currency.objects.get(symbol='RUB')
        self.wallet = create_wallet(self.user, self.rub_currency, 1000000)

        self.user_data = {'username': 'test_user2',
                          'email': 'test_user2@email.ru'}
        self.user2 = get_user_model()(**self.user_data)
        self.user2.set_password('StrongPassword123')
        self.user2.save()
        self.wallet2 = create_wallet(self.user, self.rub_currency, 1000000)

        self.user_data = {'username': 'test_user3',
                          'email': 'test_use32@email.ru'}
        self.user3_usd = get_user_model()(**self.user_data)
        self.user3_usd.set_password('StrongPassword123')
        self.user3_usd.save()
        self.usd_currency = Currency.objects.get(symbol='USD')
        self.wallet3_usd = create_wallet(self.user, self.usd_currency, 1000000)

        self.reason_income = Reason.objects.get(identifier='BASE_INCOME')
        self.reason_expense = Reason.objects.get(identifier='BASE_EXPENSE')
        self.reason_transfer = Reason.objects.get(identifier='BASE_TRANSFER')
