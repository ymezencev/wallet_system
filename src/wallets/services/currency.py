from requests import RequestException

from wallets.models import Currency
from wallets.services.cb_rates_api import get_cb_currency_rates


BASE_CURRENCY = 'RUB'


def update_currency_rates():
    """Обновление текущих курсов валют в БД"""
    try:
        rates = get_cb_currency_rates(base_currency=BASE_CURRENCY)
    except RequestException:
        # logging can't update
        return
    for symbol, rate in rates.items():
        obj, created = Currency.objects.update_or_create(
            symbol=symbol, defaults={'rate': rate})

    # logging info


def get_all_currency_rates():
    """Получение сохранённых курсов валют"""
    rates = Currency.objects.all().order_by('symbol')
    return rates


def get_currency(symbol):
    """Получаем валюту по названию"""
    if not symbol:
        return
    try:
        currency = Currency.objects.get(symbol=symbol)
    except Currency.DoesNotExist as e:
        return
    return currency
