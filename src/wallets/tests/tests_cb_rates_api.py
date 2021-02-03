from django.test import Client
from rest_framework.test import APITestCase

from wallets.services.cb_rates_api import CB_URL, get_cb_currency_rates, \
    get_cb_exchange_rate


class CBRatesAPITestCase(APITestCase):
    """Тесты API ЦБ"""

    def setUp(self):
        self.client = Client()
        self.base = 'RUB'

    def test_get_all_available_rates(self):
        """Получение всех доступных курсов валют на текщий момент API"""
        base_currency = 'RUB'
        result = get_cb_currency_rates(base_currency=base_currency)
        self.assertEquals(result['RUB'], 1)

    def test_get_all_available_rates_invalid_data(self):
        """Получаем доступные валюты, но такой базовой валюты не существует"""
        base_currency = 'AAA'
        with self.assertRaises(ValueError):
            result = get_cb_currency_rates(base_currency=base_currency)

    def test_get_exchange_rate(self):
        """Получаем обмен валют"""
        from_currency = 'RUB'
        to_currency = 'EUR'
        base_currency = 'RUB'
        result = get_cb_exchange_rate(
            from_currency, to_currency, base_currency)
        self.assertEquals(set(result.keys()), {'RUB', 'EUR'})

    def test_get_exchange_rate_invalid_data(self):
        """Получаем обмен валют, данные по валютам переданы неверно"""
        from_currency = 'RUB'
        to_currency = 'EUR'
        base_currency = 'RUB'
        with self.assertRaises(ValueError):
            result = get_cb_exchange_rate('AAA', to_currency, base_currency)
        with self.assertRaises(ValueError):
            result = get_cb_exchange_rate(from_currency, 'AAA', base_currency)
        with self.assertRaises(ValueError):
            result = get_cb_exchange_rate(from_currency, to_currency, 'AAA')

