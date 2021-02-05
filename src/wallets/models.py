import random
import string
import uuid

from django.db import models

from config import settings


class Currency(models.Model):
    """Доступные валюты и курсы """
    symbol = models.CharField(max_length=3, unique=True)
    rate = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.symbol}'


class Wallet(models.Model):
    """Кошелёк пользователя"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.CharField(max_length=12, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='wallets',
                             on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    balance = models.IntegerField(default=0)

    @staticmethod
    def _generate_serial_number():
        size = 12
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.serial_number:
            # Генерируем Serial number, если уже существует, пробуем ещё
            self.serial_number = self._generate_serial_number()
            while Wallet.objects.filter(serial_number=self.serial_number).exists():
                self.serial_number = self._generate_serial_number()
        super(Wallet, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.serial_number}: {self.balance} {self.currency.symbol}'

