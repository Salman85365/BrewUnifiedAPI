# urls.py
from django.urls import path
from .views import PriceListCreate, PriceDetail

urlpatterns = [
    path('prices/', PriceListCreate.as_view(), name='price-list-create'),
    path('prices/<int:pk>/', PriceDetail.as_view(), name='price-detail'),
]
