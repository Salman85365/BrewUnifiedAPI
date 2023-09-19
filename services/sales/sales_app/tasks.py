import requests
from celery import shared_task
from .models import Order
from django.conf import settings
from .email import send_email
import logging


@shared_task
def adjust_inventory(order_id, user_email, user_name, token):
    order = Order.objects.get(pk=order_id)

    response = requests.post(
        f"{settings.KONG_BASE_URL}/warehouse/api/items/{order.item_id}/buy/",
        headers={"Authorization": token},
        json={"ordered_quantity": order.quantity_ordered}
    )

    if response.status_code == 200:
        order.status = Order.CONFIRMED
    else:
        order.status = Order.FAILED
        logging.error(f"Failed to adjust inventory for order {order_id}. Response: {response.text}")

    order.save()
    send_email.delay(user_email, user_name, order.id, order.status)
