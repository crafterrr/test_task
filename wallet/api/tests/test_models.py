from django.test import TestCase
from api.models import Wallet, Transaction


class WalletModelTest(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet", balance=100)

    def test_wallet_creation(self):
        self.assertEqual(self.wallet.label, "Test Wallet")
        self.assertEqual(self.wallet.balance, 100)


class TransactionModelTest(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet", balance=100)
        self.transaction = Transaction.objects.create(
            wallet=self.wallet, txid="12345", amount=50
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.txid, "12345")
        self.assertEqual(self.transaction.amount, 50)

    def test_transaction_balance_update(self):
        self.transaction.amount = 30
        self.transaction.save()
        self.assertEqual(self.transaction.amount, 30)

    def test_negative_transaction_amount(self):
        self.wallet.balance = 0
        self.wallet.save()
        with self.assertRaises(ValueError):
            Transaction.objects.create(
                wallet=self.wallet, txid="54321", amount=-10
            )

    def test_negative_transaction_with_sufficient_balance(self):
        self.wallet.balance = 100
        self.wallet.save()
        transaction = Transaction.objects.create(
            wallet=self.wallet, txid="67890", amount=-50
        )
        self.assertEqual(transaction.amount, -50)
        self.assertEqual(self.wallet.balance, 50)

    def test_negative_transaction_with_insufficient_balance(self):
        self.wallet.balance = 50
        self.wallet.save()
        with self.assertRaises(ValueError):
            Transaction.objects.create(
                wallet=self.wallet, txid="9", amount=-100
            )
