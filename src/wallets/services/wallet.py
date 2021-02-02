from wallets.models import Wallet


def create_wallet(user, currency, balance):
    """Создание кошелька"""
    if balance < 0:
        raise ValueError('Начальный баланс не может быть отрицательным.')
    # info loging
    wallet = Wallet(user=user, currency=currency, balance=balance)
    wallet.save()
    return wallet


def add_money(user, amount):
    """Пополнение текущего баланса"""
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist as e:
        # logging
        raise e
    wallet.balance += amount
    wallet.save()
    # info logging
    return wallet
