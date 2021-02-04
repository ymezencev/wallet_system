from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status
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
        self.wallet = create_wallet(self.user, self.rub_currency, 0)

    def test_get_currecy_list(self):
        """Получаем список валют"""
        response = self.client.get(reverse('currency-list'))
        print(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_get_exchange_rate(self):
        """Получить курс обмена между валютами из ЦБ."""
        response = self.client.get(reverse('currency-exchange',
                                           args=('RUB', 'USD')))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data['rate'], float)

    def test_get_exchange_rate_incorrect_currency(self):
        """Получить курс обмена между валютами из ЦБ. Некорректные данные"""
        response = self.client.get(reverse('currency-exchange',
                                           args=('AAA', 'USD')))
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        response = self.client.get(reverse('currency-exchange',
                                           args=('USD', 'AAA')))
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_wallets_list(self):
        """Получаем список кошельков"""
        response = self.client.get(reverse('wallets-list'))
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_wallets_detail_by_serial(self):
        """Получаем детализация кошелька по серийному номеру"""
        response = self.client.get(
            reverse('wallets-detail', args=(self.wallet.serial_number,)))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            self.wallet.serial_number, response.data['serial_number'])

    def test_wallets_detail_by_serial_not_exists(self):
        """
        Получаем детализация кошелька по серийному номеру. Номер не существует
        """
        response = self.client.get(
            reverse('wallets-detail', args=('111111111111',)))
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_add_money(self):
        """Пополнение счёта"""
        LOGIN_DATA = {'username': self.user_data['username'],
                      'password': 'StrongPassword123'}
        self.client.post(reverse('rest_login'), LOGIN_DATA)
        data = {'amount': 100}
        balance_before = self.wallet.balance
        response = self.client.post(reverse('wallets-add-money'), data=data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        balance = Wallet.objects.get(id=self.wallet.id).balance
        self.assertEquals(balance_before+100, balance)

    def test_add_money_not_authorized_forbidden(self):
        """Пополнение счёта только авторизованный пользователь"""
        self.client.post(reverse('rest_logout'))
        data = {'amount': 100}
        response = self.client.post(reverse('wallets-add-money'), data=data)
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)
