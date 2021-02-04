from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client
from rest_framework.test import APITestCase

from wallets.models import Currency, Wallet
from wallets.services.currency import update_currency_rates
from wallets.services.wallet import create_wallet


class CurrencyTestCase(APITestCase):

    def setUp(self):
        self.client = Client()
        update_currency_rates()

        self.user_data = {'username': 'test_user',
                          'email': 'test_user@email.ru'}
        self.user = get_user_model()(**self.user_data)
        self.user.set_password('StrongPassword123')
        self.user.save()

        self.rub_currency = Currency.objects.get(symbol='RUB')

    def test_create_wallet(self):
        """Создаём кошелёк для пользователя"""
        wallet = create_wallet(self.user, self.rub_currency, 0)
        cnt = Wallet.objects.filter(id=wallet.id).count()
        self.assertEquals(cnt, 1)
        self.assertIsNotNone(wallet.serial_number)

    def test_create_wallet_incorrect_balance(self):
        """Создаём кошелёк для пользователя c неправильным балансом"""
        with self.assertRaises(ValueError):
            wallet = create_wallet(self.user, self.rub_currency, -1)
        with self.assertRaises(ValueError):
            wallet = create_wallet(self.user, self.rub_currency, 'AAAA')

    def test_create_wallet_no_user(self):
        """Создаём кошелёк без пользователя"""
        with self.assertRaises(IntegrityError):
            wallet = create_wallet(
                user=None, currency=self.rub_currency, balance=0)

    def test_create_wallet_incorrect_currency(self):
        """Создаём кошелёк с неправильной валютой"""
        with self.assertRaises(IntegrityError):
            wallet = create_wallet(
                user=self.user, currency=None, balance=0)
        with self.assertRaises(ValueError):
            wallet = create_wallet(
                user=self.user, currency='AAA', balance=0)
