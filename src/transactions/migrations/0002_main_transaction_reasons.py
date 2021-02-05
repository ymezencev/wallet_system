import datetime

from django.db import migrations, transaction

"""Создание базовые причин переводов денежных средств"""


def create_base_transaction_reasons(apps, schema_editor):

    Reason = apps.get_model('transactions', 'Reason')
    reason_add_balance = Reason(
        title='Пополнение баланса', identifier='BASE_INCOME',
        description='Базовое пополнение баланса кошелька пользователей')
    reason_add_balance.save()

    reason_minus_balance = Reason(
        title='Списание баланса', identifier='BASE_EXPENSE',
        description='Базовое списание баланса кошелька пользователей')
    reason_minus_balance.save()

    reason_transfer_maney = Reason(
        title='Денежный перевод', identifier='BASE_TRANSFER',
        description='Базовый перевод денежных средств между кошельками'
    )
    reason_transfer_maney.save()


def rollback_base_transaction_reasons(apps, schema_editor):

    Reason = apps.get_model('transactions', 'Reason')
    reason_add_balance = Reason.objects.get(identifier='BASE_INCOME')
    reason_add_balance.delete()

    reason_minus_balance = Reason.objects.get(identifier='BASE_EXPENSE')
    reason_minus_balance.delete()

    reason_transfer_maney = Reason.objects.get(identifier='BASE_TRANSFER')
    reason_transfer_maney.delte()


class Migration(migrations.Migration):
    dependencies = [('transactions', '0001_initial'), ]

    operations = [
        migrations.RunPython(
            create_base_transaction_reasons,
            rollback_base_transaction_reasons), ]
