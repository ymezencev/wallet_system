from django.db import models

from wallets.models import Wallet, Currency


class Reason(models.Model):
    """Причины переводов"""

    title = models.CharField(max_length=50)
    identifier = models.CharField(max_length=30, db_index=True)
    description = models.TextField(null=True, blank=True)


class Expense(models.Model):
    """Расходы денежных средств на кошельке"""

    wallet = models.ForeignKey(Wallet, related_name='expenses',
                               on_delete=models.DO_NOTHING)
    reason = models.ForeignKey(Reason, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.PositiveIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)


class Income(models.Model):
    """Пополнения денежных средств на кошельке"""

    wallet = models.ForeignKey(Wallet, related_name='incomes',
                               on_delete=models.DO_NOTHING)
    reason = models.ForeignKey(Reason, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.PositiveIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)


class Transaction(models.Model):
    """Переводы денежных средств"""

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    income = models.ForeignKey(Income, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
