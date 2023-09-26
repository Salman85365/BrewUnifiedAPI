from django.urls import path, include
from .views import WarehouseItemPrice, WarehouseItemBuy, WarehouseItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', WarehouseItemViewSet)

urlpatterns = [
    path('items/', include(router.urls)),
    path('items/<int:item_id>/price/', WarehouseItemPrice.as_view(),
         name='item-price'),
    path('items/<int:item_id>/buy/', WarehouseItemBuy.as_view(),
         name='item-buy')
]
