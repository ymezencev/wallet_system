import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_auth.registration.serializers import \
    RegisterSerializer as RestAuthRegisterSerializer
from rest_framework import serializers

from wallets.services.currency import get_currency
from wallets.services.wallet import create_wallet


User = get_user_model()
logger = logging.getLogger('application')


class UserLoginSerializer(RestAuthLoginSerializer):
    """Логин по username и password"""
    email = None


class UserRegisterSerializer(RestAuthRegisterSerializer):
    """Регистрация пользователя. Создание кошелька."""

    balance = serializers.IntegerField(required=True)
    currency_symbol = serializers.CharField(
        min_length=3, max_length=3, required=True)

    def validate_currency_symbol(self, currency_symbol):
        if not get_currency(symbol=currency_symbol):
            raise serializers.ValidationError(
                "Данная валюта не поддерживается.")
        return currency_symbol

    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Баланс не может быть отрицательным.")
        return value

    @transaction.atomic
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)

        currency_symbol = self.validated_data['currency_symbol']
        currency = get_currency(symbol=currency_symbol)
        balance = self.validated_data['balance']
        wallet = create_wallet(user=user, currency=currency, balance=balance)
        logger.info(f'User has registered. '
                    f'{user.id} {user.username} {user.email} '
                    f'[wallet: {wallet.serial_number}]')
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Личные данные пользователя"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', ]
