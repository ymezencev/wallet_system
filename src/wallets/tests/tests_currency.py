from django.test import Client
from rest_framework.test import APITestCase

from wallets.models import Currency
from wallets.services.currency import update_currency_rates


class CurrencyTestCase(APITestCase):

    def setUp(self):
        self.client = Client()

    def test_update_db_currencies(self):
        """Курсы валют в БД. Проверяем, что данные были обновлены"""
        update_currency_rates()
        cnt = Currency.objects.all().count()
        self.assertNotEquals(cnt, 0)
