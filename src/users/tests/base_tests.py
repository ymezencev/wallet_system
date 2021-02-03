from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase

from wallets.services.currency import update_currency_rates

User = get_user_model()

REGISTER_DATA = {
    'username': 'test_user',
    'email': 'test_user@email.ru',
    'password1': 'secretStrongPass123',
    'password2': 'secretStrongPass123',
    'balance': 0,
    'currency_symbol': 'RUB'
}

LOGIN_DATA = {
    'username': REGISTER_DATA['username'],
    'password': REGISTER_DATA['password1'],
}

REGISTER_URL = reverse('rest_register')
LOGIN_URL = reverse('rest_login')
LOGOUT_URL = reverse('rest_logout')
USER_URL = reverse('rest_user_details')


class BaseTestCase(APITestCase):
    """Тесты"""

    def setUp(self):
        self.client = Client()
        update_currency_rates()

    def register_new_user(self, n=1, balance=0, currency='RUB'):
        """
        Регистрируем нового пользователя через отправку запроса,
        где n - номер тестового пользователя
        """
        test_user_n = REGISTER_DATA.copy()
        test_user_n['username'] = f'{test_user_n["username"]}_{n}'
        test_user_n['email'] = f'{n}@'.join(test_user_n['email'].rsplit('@', 1))
        test_user_n['balance'] = balance
        test_user_n['currency_symbol'] = currency
        return self.client.post(REGISTER_URL, test_user_n)
