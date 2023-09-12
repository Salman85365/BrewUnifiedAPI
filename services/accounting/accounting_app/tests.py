from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Transaction, Account


class CustomUserTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        assert self.user is not None

        self.token_url = '/apis/token/'
        self.verify_token_url = '/apis/token/verify/'

    def _get_access_token(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass'})
        if response.status_code != status.HTTP_200_OK:
            print(response.content)
        return response.data.get('access', None)

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_authentication(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_transaction_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_access_token()}')
        account = Account.objects.create(name='Test account1', balance=1000.00)
        response = self.client.post('/apis/transactions/',
                                    {'description': 'Test transaction', 'transaction_type': 'Debit',
                                     'amount': '100.00', 'account': account.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_account_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_access_token()}')
        response = self.client.post('/apis/accounts/', {'name': 'Test account', 'transactions': '1000.00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)

    def test_token_verification(self):
        response = self.client.post(self.verify_token_url, {'token': self._get_access_token()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_user_retrieval(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_access_token()}')
        response = self.client.get('/apis/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_account_retrieval(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_access_token()}')
        response = self.client.get('/apis/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
