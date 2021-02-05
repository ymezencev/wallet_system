from requests import RequestException

from transactions.models import Transaction
from wallets.models import Wallet, Currency
from wallets.services.cb_rates_api import get_cb_exchange_rate


def transfer_money(from_wallet, to_wallet, amount, currency):
    """Перевести средства между кошельками"""
    if not isinstance(amount, int):
        raise ValueError('Неправильный формат суммы перевода')
    try:
        converted_amount = convert_currency(from_currency=from_wallet.currency,
                                            to_currency=currency,
                                            amount=amount)
    except ValueError as e:
        # logger
        pass
    except RequestException as e:
        # logger
        pass
    transfer = Transaction(from_wallet=from_wallet, to_wallet=to_wallet,
                           amount=converted_amount, currency=currency)

    transfer.save()
    return transfer


def convert_currency(from_currency, to_currency, amount):
    """Перевод валюты"""
    rate = get_cb_exchange_rate(from_currency, to_currency)
    return int(amount*rate)
