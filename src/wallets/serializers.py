from django.contrib.auth import get_user_model
from rest_framework import serializers

from wallets.models import Currency, Wallet
from wallets.services.wallet import add_money

User = get_user_model()


class CurrencyListSerializer(serializers.ModelSerializer):
    """Курс обмена валют"""
    class Meta:
        model = Currency
        fields = '__all__'


class RateExchangeSerializer(serializers.Serializer):
    """Вывод курса обмена между валютами, на основе базовой валюты"""
    rate = serializers.FloatField(read_only=True)


class WalletSerializer(serializers.ModelSerializer):
    """Кошельки пользователей"""
    username = serializers.CharField(source='user.username')
    currency = serializers.CharField(source='currency.symbol')

    class Meta:
        model = Wallet
        fields = ('id', 'serial_number', 'balance', 'user', 'username', 'currency')


class AddMoneySerializer(serializers.Serializer):
    """Пополнение баланса"""
    amount = serializers.IntegerField(required=True)


