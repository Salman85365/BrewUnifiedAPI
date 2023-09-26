from django.urls import reverse
from rest_framework.test import APITestCase
from .models import WarehouseItem
from unittest.mock import patch, Mock
from rest_framework.test import APIClient
from django.test import RequestFactory
from warehouse.middlewares import JWTAuthenticationMiddleware
from django.conf import settings


class MockUser:
    """Mock user to represent user data from authentication service."""

    def __init__(self, username, role):
        self.username = username
        self.role = role


class WarehouseItemTests(APITestCase):
    def setUp(self):
        self.item = WarehouseItem.objects.create(
            name="TestItem",
            description="A test item",
            quantity=100,
            price=20.00
        )
        self.client = APIClient()
        self.factory = RequestFactory()
        self.middleware = JWTAuthenticationMiddleware(
            lambda req: Mock(status_code=200))
        self.admin_user = MockUser(username='admin', role='Admin')
        self.normal_user = MockUser(username='user', role='User')
        settings.KONG_BASE_URL = "mocked_url"

    @patch("warehouse.middlewares.cache.get")
    @patch("warehouse.middlewares.cache.set")
    @patch("warehouse.middlewares.requests.post")
    def test_valid_token_not_in_cache(self, mock_post, mock_cache_set,
                                      mock_cache_get):
        mock_post.return_value = Mock(status_code=200,
                                      json=lambda: {"data": "user_data"})
        mock_cache_get.return_value = None
        request = self.factory.get('/some_path',
                                   HTTP_AUTHORIZATION='Bearer valid_token')
        response = self.middleware(request)
        mock_cache_set.assert_called()
        self.assertEqual(response.status_code, 200)

    def test_request_to_admin_site(self):
        request = self.factory.get('/admin/some_path')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_successful_buy(self, mock_valid_token):
        data = {"ordered_quantity": 5}
        response = self.client.post(reverse('item-buy', args=[self.item.id]),
                                    data,
                                    HTTP_AUTHORIZATION='Bearer test_token')

        self.assertEqual(response.status_code, 200)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_list_items(self, mock_valid_token):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get('/api/items/',
                                   HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 200)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "Admin"}}, 200))
    def test_admin_can_add_item(self, mock_valid_token):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/items/add-item/', {
            'name': 'New Item', 'price': 50, 'quantity': 10},
                                    HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 201)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "User"}}, 200))
    def test_non_admin_cannot_add_item(self, mock_valid_token):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post('/api/items/add-item/', {
            'name': 'New Item', 'price': 50, 'quantity': 10},
                                    HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 403)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "Admin"}}, 200))
    def test_admin_can_update_price(self, mock_valid_token):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f'/api/items/{self.item.id}/price/',
                                   {'price': 150},
                                   HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 200)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "User"}}, 200))
    def test_non_admin_cannot_update_price(self, mock_valid_token):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'/api/items/{self.item.id}/price/',
                                   {'price': 150},
                                   HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 403)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "User"}}, 200))
    def test_user_can_buy(self, mock_valid_token):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(f'/api/items/{self.item.id}/buy/',
                                    {'ordered_quantity': 3},
                                    HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 200)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "User"}}, 200))
    def test_user_cannot_buy_more_than_available(self, mock_valid_token):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(f'/api/items/{self.item.id}/buy/',
                                    {'ordered_quantity': 1000},
                                    HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 400)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": {"role": "User"}}, 200))
    def test_buying_reduces_quantity(self, mock_valid_token):
        self.client.force_authenticate(user=self.normal_user)
        self.client.post(f'/api/items/{self.item.id}/buy/',
                         {'ordered_quantity': 3},
                         HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 100 - 3)
