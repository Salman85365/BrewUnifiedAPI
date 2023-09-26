import requests
from django.conf import settings


def request_item_detail(item_id, token):
    response = requests.get(
        f"{settings.KONG_BASE_URL}/warehouse/api/items/{item_id}/",
        headers={"Authorization": token}
    )
    if response.status_code == 200:
        return response.json()
    return None


def request_balance_deduction(user_id, amount, token):
    response = requests.post(
        f"{settings.KONG_BASE_URL}/accounting/api/transactions/",
        data={
            "transaction_type": "Debit", "amount": amount, "account": user_id
        },
        headers={"Authorization": token}
    )
    if response.status_code == 201:
        return True
    return False
