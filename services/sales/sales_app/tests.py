from django.test import TestCase
from rest_framework.test import APIClient
from .models import Sale, Order

class SaleListCreateTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_sale_valid_data(self):
        response = self.client.post('/path_to_sale_endpoint/', {
            # Replace with a valid data structure that matches SaleSerializer's requirements
            # 'field_name': 'value',
        })
        self.assertEqual(response.status_code, 201)
        # Add more assertions based on your serializer's fields

    def test_create_sale_invalid_data(self):
        response = self.client.post('/path_to_sale_endpoint/', {
            # Provide invalid data
            # 'field_name': 'invalid_value',
        })
        self.assertEqual(response.status_code, 400)

    def test_cache_invalidation_after_sale(self):
        # Make a sale
        self.client.post('/path_to_sale_endpoint/', {
            # 'field_name': 'value',
        })

        # Check if cache is invalidated
        # You'd typically use a mocking framework like `mock` or `unittest.mock` to verify the cache's delete method was called.
        # For simplicity, just checking the key directly:
        from django.core.cache import cache
        self.assertIsNone(cache.get("items_key"))


class OrderCreateTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_order(self):
        response = self.client.post('/path_to_order_endpoint/', {
            'item_id': '1',
            'item_name': 'ItemName',
            'quantity_ordered': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_order_without_item_name(self):
        response = self.client.post('/path_to_order_endpoint/', {
            'item_id': '1',
            'quantity_ordered': 2
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_order_without_item_id(self):
        response = self.client.post('/path_to_order_endpoint/', {
            'item_name': 'ItemName',
            'quantity_ordered': 2
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_adjust_inventory_called(self):
        # Using `unittest.mock` to check if the adjust_inventory Celery task is called
        from unittest.mock import patch

        with patch('path_to_your_tasks_module.adjust_inventory.delay') as mocked_task:
            self.client.post('/path_to_order_endpoint/', {
                'item_id': '1',
                'item_name': 'ItemName',
                'quantity_ordered': 2
            })
            self.assertTrue(mocked_task.called)
