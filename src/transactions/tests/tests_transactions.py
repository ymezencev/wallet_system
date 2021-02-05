from transactions.models import Income, Expense, Transaction
from transactions.services.transactions import create_income, TransactionError, \
    create_expense, transfer_money
from transactions.tests.base_tests import BaseTestCase
from wallets.models import Wallet
from wallets.services.currency import get_currency_exchange_amount


class TransactionsTestCase(BaseTestCase):
    """Тесты транзакций"""

    def test_add_money(self):
        """Пополнение баланса"""
        old_balance = self.wallet.balance
        income = create_income(self.wallet, self.reason_income, 770)

        wallet = Wallet.objects.get(
            serial_number=self.wallet.serial_number)
        income_cnt = Income.objects.filter(id=income.id).count()
        self.assertEquals(1, income_cnt)
        self.assertEquals(old_balance+770, wallet.balance)

    def test_add_money_incorrect_amount(self):
        """Пополнение баланса. Некорректная сумма пополнения"""
        with self.assertRaises(TransactionError):
            create_income(self.wallet, self.reason_income, -100)
        with self.assertRaises(TransactionError):
            create_income(self.wallet, self.reason_income, 'AAA')

    def test_add_money_incorrect_reason(self):
        """Пополнение баланса. Некорректная причина"""
        with self.assertRaises(TransactionError):
            create_income(self.wallet, 1111, 100)
        with self.assertRaises(TransactionError):
            create_income(self.wallet, 'aaaaa', 100)

    def test_add_money_incorrect_wallet(self):
        """Пополнение баланса. Несуществубщий кошелёк"""
        with self.assertRaises(TransactionError):
            create_income(111, self.reason_income, 100)
        with self.assertRaises(TransactionError):
            create_income('aaa', self.reason_income, 100)

    def test_minus_money(self):
        """Списание баланса"""
        old_balance = self.wallet.balance
        expense = create_expense(self.wallet, self.reason_expense, 77)

        wallet = Wallet.objects.get(
            serial_number=self.wallet.serial_number)
        expense_cnt = Expense.objects.filter(id=expense.id).count()
        self.assertEquals(1, expense_cnt)
        self.assertEquals(old_balance-77, wallet.balance)

    def test_minus_money_incorrect_amount(self):
        """Списание баланса. Некорректная сумма пополнения"""
        with self.assertRaises(TransactionError):
            create_expense(self.wallet, self.reason_income, -100)
        with self.assertRaises(TransactionError):
            create_expense(self.wallet, self.reason_income, 'AAA')

    def test_minus_money_incorrect_reason(self):
        """Списание баланса. Некорректная причина"""
        with self.assertRaises(TransactionError):
            create_expense(self.wallet, 1111, 100)
        with self.assertRaises(TransactionError):
            create_expense(self.wallet, 'aaaaa', 100)

    def test_minus_money_incorrect_wallet(self):
        """Списание баланса. Несуществубщий кошелёк"""
        with self.assertRaises(TransactionError):
            create_expense(111, self.reason_income, 100)
        with self.assertRaises(TransactionError):
            create_expense('aaa', self.reason_income, 100)

    def test_transfer_money(self):
        """
        Перевод. валюты кошельков: руб -> руб (переводим 5 руб)
        """
        balance_before_wallet = self.wallet.balance
        balance_before_wallet2 = self.wallet2.balance
        transfer = transfer_money(
            self.wallet, self.wallet2, 500, self.rub_currency)
        self.wallet.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEquals(balance_before_wallet-500, self.wallet.balance)
        self.assertEquals(balance_before_wallet2+500, self.wallet2.balance)
        expense_cnt = Expense.objects.filter(id=transfer.expense.id).count()
        self.assertEquals(1, expense_cnt)
        income_cnt = Income.objects.filter(id=transfer.income.id).count()
        self.assertEquals(1, income_cnt)
        transfer_cnt = Transaction.objects.filter(id=transfer.id).count()
        self.assertEquals(1, transfer_cnt)

    def test_transfer_money_different_currency(self):
        """
        Перевод. валюты кошельков: руб -> руб (переводим 10 баксов)
        """
        balance_before_wallet = self.wallet.balance
        balance_before_wallet2 = self.wallet2.balance
        transfer_money(from_wallet=self.wallet, to_wallet=self.wallet2,
                       amount=1000,  currency=self.usd_currency)
        self.wallet.refresh_from_db()
        self.wallet2.refresh_from_db()
        amount_rub = get_currency_exchange_amount(
            self.usd_currency.symbol, self.wallet.currency.symbol, 1000)
        self.assertEquals(
            balance_before_wallet-amount_rub, self.wallet.balance)
        self.assertEquals(
            balance_before_wallet2+amount_rub, self.wallet2.balance)

    def test_transfer_money_usd_to_rub(self):
        """
        Перевод. валюты кошельков: бакс -> руб (переводим 10 руб)
        """
        balance_before_wallet3 = self.wallet3_usd.balance
        balance_before_wallet2 = self.wallet2.balance
        transfer_money(from_wallet=self.wallet3_usd, to_wallet=self.wallet2,
                       amount=1000,  currency=self.rub_currency)
        self.wallet3_usd.refresh_from_db()
        self.wallet2.refresh_from_db()
        amount_usd = get_currency_exchange_amount(
            self.rub_currency.symbol, self.wallet3_usd.currency.symbol, 1000)

        self.assertEquals(
            balance_before_wallet3-amount_usd, self.wallet3_usd.balance)
        self.assertEquals(
            balance_before_wallet2+1000, self.wallet2.balance)

    def test_transfer_money_too_small_amount(self):
        """Перевод кошельки руб -> бакс (1 руб). Недостаточная сумма"""
        with self.assertRaises(TransactionError):
            transfer_money(from_wallet=self.wallet, to_wallet=self.wallet3_usd,
                           amount=1,  currency=self.rub_currency)

    def test_transfer_not_enough_money(self):
        """Перевод недостаточно средств"""
        balance_before_wallet = self.wallet.balance
        with self.assertRaises(TransactionError):
            transfer_money(from_wallet=self.wallet, to_wallet=self.wallet3_usd,
                           amount=100000000000000,  currency=self.usd_currency)

        self.wallet.refresh_from_db()
        self.assertEquals(balance_before_wallet, self.wallet.balance)
