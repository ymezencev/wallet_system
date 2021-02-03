from django.contrib.auth import get_user_model
from rest_framework import status

from users.tests.base_tests import REGISTER_URL, REGISTER_DATA, LOGIN_URL, \
    LOGIN_DATA, BaseTestCase
from wallets.models import Wallet

User = get_user_model()


class UserAuthRegisterTestCase(BaseTestCase):
    """Тесты регистрации пользователя"""

    def test_register_success(self):
        """Тест успешной регистрации"""
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        user_cnt = User.objects.filter(
            username=REGISTER_DATA['username']).count()
        self.assertEquals(user_cnt, 1)
        wallet_cnt = Wallet.objects.filter(
            user__username=REGISTER_DATA['username']).count()
        self.assertEquals(wallet_cnt, 1)

    def test_register_currency_not_exists(self):
        """Тест регистрации, передана неправильная валюта"""
        response = self.register_new_user(n=1, balance=0, currency='AAA')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_currency_incorrect_format(self):
        """Тест регистрации, валюта 3 символа"""
        response = self.register_new_user(n=2, balance=0, currency='AAAAA')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.register_new_user(n=3, balance=0, currency='A')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_incorrect_start_balance(self):
        """Тест регистрации, баланс стартовый некорректен"""
        response = self.register_new_user(n=4, balance=-1)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.register_new_user(n=5, balance='aaaaa')
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_not_all_data_passed(self):
        """Тест регистрации, переданы не все данные"""
        data = {'username': 'test_error773',
                'email': 'test_error773@email.ru',
                'password1': 'secretStrongPass123',
                'password2': 'secretStrongPass123'}
        response = self.client.post(REGISTER_URL, data)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)


class UserAuthLoginTestCase(BaseTestCase):
    """Тесты авторизации пользователя"""

    def setUp(self):
        super().setUp()
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_login_success(self):
        """Тест успешной авторизации"""
        response = self.client.post(LOGIN_URL, LOGIN_DATA)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data.get('key'))

    def test_login_failure_incorrect_password(self):
        """Авторизация не успешна, неправильный пароль"""
        test_user_data = LOGIN_DATA.copy()
        test_user_data['password'] = 'incorrect_password'
        response = self.client.post(LOGIN_URL, test_user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_login_failure_user_not_exist(self):
        """Авторизация не успешна, пользователь не существует"""
        test_user_data = {'username': 'non_existent_user',
                          'password': 'incorrect_password'}
        response = self.client.post(LOGIN_URL, test_user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
