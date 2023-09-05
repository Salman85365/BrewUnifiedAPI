from django.urls import path
from .views import WarehouseItemList, WarehouseItemPrice, WarehouseItemBuy, CreateDummyDataWarehouse

urlpatterns = [
    path('items/', WarehouseItemList.as_view(), name='item-list'),
    path('items/<int:item_id>/price/', WarehouseItemPrice.as_view(), name='item-price'),
    path('items/<int:item_id>/buy/', WarehouseItemBuy.as_view(), name='item-buy'),
    path('items/create-dummy-data/', CreateDummyDataWarehouse.as_view(), name='create-dummy-data'),
]
