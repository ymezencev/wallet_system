import logging

from wallets.models import Wallet


logger = logging.getLogger('wallets')


def create_wallet(user, currency, balance):
    """Создание кошелька"""
    if balance < 0:
        raise ValueError('Начальный баланс не может быть отрицательным.')
    wallet = Wallet(user=user, currency=currency, balance=balance)
    wallet.save()
    logger.info(
        f'Wallet created. user id: {user.id} serial: {wallet.serial_number} '
        f'sum: {wallet.balance} {wallet.currency.symbol}.')
    return wallet


def add_money(user, amount):
    """Пополнение текущего баланса"""
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist as e:
        logger.error(f'Error add money. user id{user.id} '
                     f'Wallet not found. {e}')
        raise e
    wallet.balance += amount
    wallet.save()
    logging.info(f'Add money {amount} {wallet.currency.symbol} '
                 f'to wallet {wallet.serial_number}')
    return wallet
