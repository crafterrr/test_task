from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Wallet, Transaction
from django.conf import settings


class WalletListTestCase(APITestCase):
    def test_get_wallets(self):
        response = self.client.get('/api/wallet/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json().get('results', []), list)

    def test_create_wallet(self):
        data = {'label': 'Test Wallet'}
        response = self.client.post('/api/wallet/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        self.assertEqual(response.json()['label'], 'Test Wallet')

    def test_create_wallet_invalid_data(self):
        data = {'label': ''}
        response = self.client.post('/api/wallet/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_search(self):
        for i in range(1, 6):
            Wallet.objects.create(label=f"Wallet_{i}", balance=100 * i)

        response = self.client.get('/api/wallet/?label=Wallet_3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['label'], 'Wallet_3')

    def test_wallet_pagination(self):
        for i in range(1, 6):
            Wallet.objects.create(label=f"Wallet_{i}", balance=100 * i)

        response = self.client.get('/api/wallet/?page_number=2&page_length=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['label'], 'Wallet_3')
        self.assertEqual(results[1]['label'], 'Wallet_4')


class TransactionListTestCase(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet", balance=100)

    def test_get_transactions(self):
        response = self.client.get('/api/transaction/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json().get('results', []), list)

    def test_create_transaction(self):
        data = {
            'wallet': {'type': 'Wallet', 'id': str(self.wallet.id)},
            'txid': 'Test TXID',
            'amount': 10
        }
        response = self.client.post('/api/transaction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        self.assertEqual(response.json()['txid'], 'Test TXID')
        self.assertEqual(response.json()['amount'], '10.00')

    def test_create_transaction_duplicate(self):
        data = {
            'wallet': {'type': 'Wallet', 'id': str(self.wallet.id)},
            'txid': 'Test TXID',
            'amount': 10
        }
        response = self.client.post('/api/transaction/', data, format='json')

        data = {
            'wallet': {'type': 'Wallet', 'id': str(self.wallet.id)},
            'txid': 'Test TXID',
            'amount': 10
        }
        response = self.client.post('/api/transaction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_invalid_data(self):
        data = {
            'wallet': {'type': 'Wallet', 'id': str(self.wallet.id)},
            'txid': '',
            'amount': 10
        }
        response = self.client.post('/api/transaction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transaction_pagination(self):
        for i in range(settings.PAGE_SIZE + 10):
            Transaction.objects.create(wallet=self.wallet, txid=f"TXID_{i}", amount=10)

        response = self.client.get('/api/transaction/?page_number=1')
        self.assertEqual(len(response.json()['results']), settings.PAGE_SIZE)

        response = self.client.get('/api/transaction/?page_number=2')
        self.assertEqual(len(response.json()['results']), 10)

    def test_transaction_filtering(self):
        Transaction.objects.create(wallet=self.wallet, txid="FILTER_TEST_1", amount=10)
        Transaction.objects.create(wallet=self.wallet, txid="FILTER_TEST_2", amount=20)

        response = self.client.get('/api/transaction/?txid=FILTER_TEST_1')
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['txid'], "FILTER_TEST_1")

        response = self.client.get('/api/transaction/?txid=FILTER_TEST_2')
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['txid'], "FILTER_TEST_2")

    def test_transaction_ordering(self):
        Transaction.objects.create(wallet=self.wallet, txid="ORDER_TEST_1", amount=30)
        Transaction.objects.create(wallet=self.wallet, txid="ORDER_TEST_2", amount=10)
        Transaction.objects.create(wallet=self.wallet, txid="ORDER_TEST_3", amount=20)

        response = self.client.get('/api/transaction/?ordering=amount')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(results[0]['amount'], '10.00')
        self.assertEqual(results[1]['amount'], '20.00')
        self.assertEqual(results[2]['amount'], '30.00')

        response = self.client.get('/api/transaction/?ordering=-amount')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(results[0]['amount'], '30.00')
        self.assertEqual(results[1]['amount'], '20.00')
        self.assertEqual(results[2]['amount'], '10.00')
