import unittest
from unittest.mock import patch, Mock, MagicMock
from rest_framework.test import APIClient
from django.test import RequestFactory
from sales.middlewares import JWTAuthenticationMiddleware
from django.conf import settings


class JWTAuthenticationMiddlewareTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.middleware = JWTAuthenticationMiddleware(
            lambda req: Mock(status_code=200))
        settings.KONG_BASE_URL = "mocked_url"  # mock KONG_BASE_URL for tests

    @patch("sales.middlewares.cache.get")
    @patch("sales.middlewares.cache.set")
    @patch("sales.middlewares.requests.post")
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

    @patch("sales.middlewares.cache.get")
    def test_valid_token_in_cache(self, mock_cache_get):
        mock_cache_get.return_value = {"data": "user_data"}
        request = self.factory.get('/some_path',
                                   HTTP_AUTHORIZATION='Bearer valid_token')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    @patch("sales.middlewares.cache.get")
    @patch("sales.middlewares.requests.post")
    def test_invalid_token(self, mock_post, mock_cache_get):
        mock_post.return_value = Mock(status_code=401, json=lambda: {
            "detail": "Token is invalid or expired"})
        mock_cache_get.return_value = None
        request = self.factory.get('/some_path',
                                   HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 401)

    def test_no_token(self):
        request = self.factory.get('/some_path')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 401)

    def test_request_to_admin_site(self):
        request = self.factory.get('/admin/some_path')
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    @patch('sales.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    @patch('sales_app.tasks.adjust_inventory.delay',
           return_value=MagicMock(name="Mocked method"))  # Add this line
    def test_create_order(self, mock_valid_token,
                          mocked_task):  # Add mocked_task
        response = self.client.post('/api/orders/', {
            'item_id': '1',
            'item_name': 'ItemName',
            'quantity_ordered': 2
        }, HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    @patch('sales.middlewares.JWTAuthenticationMiddleware.is_valid_token',
           return_value=(True, {"data": "mocked_data"}, 200))
    @patch('sales_app.views.cache')
    def test_create_sale(self, mock_cache, mock_valid_token):
        url = '/api/sales/'
        data = {'item': 'test_item', 'quantity_sold': 5}
        response = self.client.post(url, data, format='json',
                                    HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('item'), data.get('item'))
        self.assertEqual(response.data.get('quantity_sold'),
                         data.get('quantity_sold'))
        # if you need to check the ID exists (for example)
        self.assertTrue('id' in response.data)


if __name__ == "__main__":
    unittest.main()
