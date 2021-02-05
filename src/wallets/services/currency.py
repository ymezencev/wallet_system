import logging

from requests import RequestException

from wallets.models import Currency
from wallets.services.cb_rates_api import get_cb_currency_rates, \
    get_cb_exchange_rate

logger = logging.getLogger('wallets')
BASE_CURRENCY = 'RUB'


def update_currency_rates():
    """Обновление текущих курсов валют в БД"""
    try:
        rates = get_cb_currency_rates(base_currency=BASE_CURRENCY)
    except RequestException:
        logger.info(f'Currency rates were NOT updated. API not available.')
        return
    for symbol, rate in rates.items():
        Currency.objects.update_or_create(
            symbol=symbol, defaults={'rate': rate})
    logger.info(f'Currency rates were updated')


def get_all_currency_rates():
    """Получение сохранённых курсов валют"""
    rates = Currency.objects.all().order_by('symbol')
    return rates


def get_currency(symbol):
    """Получаем валюту по названию или None"""
    if not symbol:
        return
    try:
        currency = Currency.objects.get(symbol=symbol)
    except Currency.DoesNotExist:
        return
    return currency


def get_currency_exchange_amount(from_currency, to_currency, amount):
    """Получаем сумму обмена валюты"""
    if from_currency == to_currency:
        rate = 1
    else:
        rate = get_cb_exchange_rate(from_currency, to_currency)
    result = int(amount*rate)
    if result < 1:
        raise ValueError('Недопустимая сумма перевода')
    return result
