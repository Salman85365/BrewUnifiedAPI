import requests
from celery import shared_task
from .models import Order
from django.conf import settings


@shared_task
def adjust_inventory(order_id):
    order = Order.objects.get(pk=order_id)
    item_id = order.item_id
    quantity_ordered = order.quantity_ordered

    # Make a call to the warehouse service to reduce the quantity
    response = requests.post(
        f"{settings.KONG_BASE_URL}/warehouse/items/{item_id}/buy/",
        json={
            "ordered_quantity": quantity_ordered
        }
    )
    if response.status_code != 200:
        raise ValueError(f"Failed to adjust inventory for item {item_id}.")
