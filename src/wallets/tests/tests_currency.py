from django.test import Client
from rest_framework.test import APITestCase

from wallets.models import Currency
from wallets.services.currency import update_currency_rates, \
    get_currency_exchange_amount


class CurrencyTestCase(APITestCase):

    def setUp(self):
        self.client = Client()

    def test_update_db_currencies(self):
        """Курсы валют в БД. Проверяем, что данные были обновлены"""
        update_currency_rates()
        cnt = Currency.objects.all().count()
        self.assertNotEquals(cnt, 0)

    def test_currency_exchange_amount(self):
        """Сумма в другой валюте"""
        amount = get_currency_exchange_amount('USD', 'RUB', 10)
        self.assertGreater(amount, 0)
