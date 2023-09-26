import requests
from celery import shared_task
from .models import Order, Sale
from django.conf import settings
import logging


@shared_task
def adjust_inventory(order_id, token):
    order = Order.objects.get(pk=order_id)

    response = requests.post(
        f"{settings.KONG_BASE_URL}/warehouse/api/items/{order.item_id}/buy/",
        headers={"Authorization": token},
        json={"ordered_quantity": order.quantity_ordered}
    )

    if response.status_code == 200:
        Sale.objects.create(item=order.item_name,
                            quantity_sold=order.quantity_ordered)
    else:
        order.status = Order.FAILED
        logging.error(
            f"Failed to adjust inventory for order {order_id}. Response: "
            f"{response.text}")

    order.save()
