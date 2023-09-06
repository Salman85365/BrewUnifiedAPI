# urls.py
from django.urls import path
from .views import SaleListCreate, OrderCreate

urlpatterns = [
    path('sales/', SaleListCreate.as_view(), name='sale-list-create'),
    path('orders/', OrderCreate.as_view(), name='order-create'),
]
