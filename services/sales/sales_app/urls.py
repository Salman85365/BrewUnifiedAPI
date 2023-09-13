# urls.py
from django.urls import path
from .views import SaleListCreate

urlpatterns = [
    path('sales/', SaleListCreate.as_view(), name='sale-list-create'),
]
