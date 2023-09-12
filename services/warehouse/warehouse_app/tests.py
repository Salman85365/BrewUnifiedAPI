from django.urls import reverse
from rest_framework.test import APITestCase
# from unittest.mock import patch
from .models import WarehouseItem
import unittest
from unittest.mock import patch, Mock
from rest_framework.test import APIClient
from django.test import RequestFactory
from warehouse.middlewares import JWTAuthenticationMiddleware
from django.conf import settings


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
        self.middleware = JWTAuthenticationMiddleware(lambda req: Mock(status_code=200))
        settings.KONG_BASE_URL = "mocked_url"

    @patch("warehouse.middlewares.cache.get")
    @patch("warehouse.middlewares.cache.set")
    @patch("warehouse.middlewares.requests.post")
    def test_valid_token_not_in_cache(self, mock_post, mock_cache_set, mock_cache_get):
        mock_post.return_value = Mock(status_code=200, json=lambda: {"data": "user_data"})
        mock_cache_get.return_value = None
        request = self.factory.get('/some_path', HTTP_AUTHORIZATION='Bearer valid_token')
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
        response = self.client.post(reverse('item-buy', args=[self.item.id]), data,
                                    HTTP_AUTHORIZATION='Bearer test_token')

        self.assertEqual(response.status_code, 200)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_update_item_price(self, mock_valid_token):

        data = {"price": 150}
        response = self.client.put(reverse('item-price', args=[self.item.id]), data,
                                   HTTP_AUTHORIZATION='Bearer test_token')

        self.assertEqual(response.status_code, 200)


    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_retrieve_warehouse_items(self, mock_valid_token):
        response = self.client.get(reverse('item-list'), HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 200)
    #
    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_create_warehouse_item(self, mock_valid_token):
        data = {
            'name': 'NewItem',
            'description': 'A new test item',
            'quantity': 50,
            'price': 10.00
        }
        response = self.client.post(reverse('item-list'), data, HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 201)
    #
    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_update_item_price(self, mock_valid_token):
        data = {'price': 25.00}
        response = self.client.put(reverse('item-price', args=[self.item.id]), data, HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('price'), 25.00)


    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_unsuccessful_buy(self, mock_valid_token):
        data = {'ordered_quantity': 105}
        response = self.client.post(reverse('item-buy', args=[self.item.id]), data, HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 400)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token', return_value=(False, {"detail": "Token is invalid or expired"}, 401))
    def test_invalid_token(self, mock_valid_token):
        response = self.client.get(reverse('item-list'), HTTP_AUTHORIZATION='Bearer InvalidToken')
        self.assertEqual(response.status_code, 401)

    def test_missing_token(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 401)

    def test_admin_bypass_jwt(self):
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 401)

    @patch('warehouse.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    def test_invalid_payload_create(self, mock_valid_token):
        data = {
            'name': '',
            'quantity': 50,
            'price': 10.00
        }
        response = self.client.post(reverse('item-list'), data, HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 400)


