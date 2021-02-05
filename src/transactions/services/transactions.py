import logging

from django.db import transaction, IntegrityError
from requests import RequestException

from transactions.models import Transaction, Expense, Reason, Income
from wallets.models import Wallet
from wallets.services.currency import get_currency_exchange_amount


logger = logging.getLogger('transactions')


class TransactionError(Exception):
    """Исключение при переводе денежных средств"""
    pass


@transaction.atomic
def create_expense(wallet, reason, amount):
    """Расход денежных средств в валюте кошелька"""

    if not isinstance(amount, int) or amount <= 0:
        logger.error(f'Неправильный формат суммы перевода. amount: {amount}')
        raise TransactionError('Неправильный формат суммы перевода.')

    try:
        wallet = Wallet.objects.get(id=wallet.id)
    except (ValueError, AttributeError, Wallet.DoesNotExist) as e:
        logger.error(f'При списании баланса не найден кошелёк. {e}')
        raise TransactionError('При списании баланса не найден кошелёк.')

    wallet.balance -= amount
    wallet.save()
    currency = wallet.currency
    try:
        expense = Expense.objects.create(
            wallet=wallet, reason=reason, amount=amount, currency=currency)
    except (ValueError, IntegrityError) as e:
        logger.error(
            f'Ошибка списания средств при создании записи о расходах. {e}')
        raise TransactionError('Ошибка списания средств.')

    logger.info(f'С кошелька {wallet.serial_number} были списаны средства: '
                f'{amount} {currency.symbol}')
    return expense


@transaction.atomic
def create_income(wallet, reason, amount):
    """Пополнение денежных средств в валюте кошелька"""

    if not isinstance(amount, int) or amount <= 0:
        logger.error(f'Неправильный формат суммы перевода. amount: {amount}')
        raise TransactionError('Неправильный формат суммы перевода.')

    try:
        wallet = Wallet.objects.get(id=wallet.id)
    except (ValueError, AttributeError, Wallet.DoesNotExist) as e:
        logger.error(f'При пополнении баланса не найден кошелёк. {e}')
        raise TransactionError('При пополнении баланса не найден кошелёк.')

    wallet.balance += amount
    wallet.save()
    currency = wallet.currency
    try:
        income = Income.objects.create(
            wallet=wallet, reason=reason, amount=amount, currency=currency)
    except (ValueError, IntegrityError) as e:
        logger.error(
            f'Ошибка пополнения средств при создании записи о пополнении. {e}')
        raise TransactionError('Ошибка пополнения средств.')

    logger.info(f'На кошелёк {wallet.serial_number} были зачислены средства: '
                f'{amount} {currency.symbol}')
    return income


@transaction.atomic
def transfer_money(from_wallet, to_wallet, amount, currency):
    """Перевести средства между кошельками"""
    if not isinstance(amount, int) or amount <= 0:
        raise ValueError(f'Неправильный формат суммы перевода: {amount}')

    try:
        amount_expense = get_currency_exchange_amount(
            currency.symbol, from_wallet.currency.symbol, amount)
        amount_income = get_currency_exchange_amount(
            currency.symbol, to_wallet.currency.symbol, amount)
    except (ValueError, AttributeError) as e:
        logger.error(
            f'Ошибка при получении курса обмена валют. {e}')
        raise TransactionError(
            'Ошибка при получении курса обмена валют.')
    except RequestException as e:
        logger.error(
            f'Не удалось получить обмен валют. Сервис не доступен. {e}')
        raise TransactionError(
            'Не удалось получить обмен валют. Сервис не доступен.')

    try:
        reason = Reason.objects.get(identifier='BASE_TRANSFER')
    except Reason.DoesNotExist as e:
        logger.error(f'Не найдена причина перевода. {e}')
        raise TransactionError('Не найдена причина перевода.')

    if from_wallet.balance - amount_expense <= 0:
        raise TransactionError('Недостаточно денежных средста для перевода.')

    try:
        expense = create_expense(
            wallet=from_wallet, reason=reason, amount=amount_expense)
        income = create_income(
            wallet=to_wallet, reason=reason, amount=amount_income)
    except TransactionError as e:
        logger.error(f'Ошибка во время перевода денежных средств. {e}')
        raise e

    try:
        transfer = Transaction.objects.create(expense=expense, income=income)
    except (ValueError, IntegrityError) as e:
        logger.error(f'Ошибка сохранения записи о переводе. {e}')
        raise TransactionError('Ошибка во время перевода денежных средств.')

    logger.info(
        f'Перевод денежных средств. {amount} {currency.symbol} '
        f'from: {from_wallet.serial_number} to {to_wallet.serial_number} ')
    return transfer
