from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Transaction, Account


class TransactionsTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   password='testpass',
                                                   email='test@example.com')
        self.admin = CustomUser.objects.create_superuser(username='admin',
                                                         password='admin',
                                                         role=CustomUser.ADMIN)
        self.account = Account.objects.create(name='TestAccount', balance=1000,
                                              user=self.user)
        self.transaction = Transaction.objects.create(
            description="Sample Transaction",
            transaction_type=Transaction.DEBIT,
            account=self.account,
            amount=100
        )
        self.client.force_authenticate(user=self.user)
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_staff)

        assert self.user is not None

        self.token_url = '/api/token/'
        self.verify_token_url = '/api/token/verify/'

    def _get_access_token(self):
        response = self.client.post(self.token_url, {
            'username': 'testuser', 'password': 'testpass'})
        if response.status_code != status.HTTP_200_OK:
            print(response.content)
        return response.data.get('access', None)

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_user_authentication(self):
        response = self.client.post(self.token_url, {
            'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_transaction_list(self):
        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transaction_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "description": "Another Transaction",
            "transaction_type": Transaction.CREDIT,
            "account": self.account.id,
            "amount": 100
        }
        response = self.client.post('/api/transactions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_transaction_non_admin(self):
        data = {
            "amount": 200
        }
        response = self.client.put(f'/api/transactions/{self.transaction.id}/',
                                   data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_transaction_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "amount": 200
        }
        response = self.client.patch(
            f'/api/transactions/{self.transaction.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test',
                                                   password='test')
        self.admin = CustomUser.objects.create_superuser(username='admin',
                                                         password='admin',
                                                         role=CustomUser.ADMIN)
        self.account = Account.objects.create(name='TestAccount', balance=1000,
                                              user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_account_list(self):
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account_non_admin(self):
        data = {
            "name": "Another Account",
            "balance": 1500,
            "user": self.user
        }
        response = self.client.post('/api/accounts/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_account_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "name": "Another Account",
            "balance": 1500,
            "user": self.admin.id
        }
        response = self.client.post('/api/accounts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_account_non_admin(self):
        data = {
            "balance": 2000,
            "user": self.user
        }
        response = self.client.put(f'/api/accounts/{self.account.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_account_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "balance": 2000,
        }
        response = self.client.patch(f'/api/accounts/{self.account.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
