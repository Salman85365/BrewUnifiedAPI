from django.core.cache import cache
from .models import Sale, Order
from .serializers import SaleSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import adjust_inventory
from rest_framework import status
from .utils import request_item_detail, request_balance_deduction
from .email import send_email


def get_or_set_cache(key, model, serializer_cls):
    cached_data = cache.get(key)
    if cached_data:
        return Response(cached_data)

    items = model.objects.all()
    serializer = serializer_cls(items, many=True)
    cache.set(key, serializer.data)
    return Response(serializer.data)


class SaleListCreate(APIView):
    def get(self, request):
        return get_or_set_cache("sales_key", Sale, SaleSerializer)

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("sales_key")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


SUCCESS = 'success'
FAILED = 'failed'


class OrderCreate(APIView):
    def get(self, request):
        return get_or_set_cache("orders_key", Order, OrderSerializer)

    def post(self, request):
        user_data = request.user_data
        token = request.META.get("HTTP_AUTHORIZATION")

        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save(status=Order.PENDING)

        if not self.is_item_available(order, token):
            return self.set_order_failed(order,
                                         'Insufficient quantity available.')

        if not self.has_sufficient_balance(order, user_data):
            return self.set_order_failed(order, 'Insufficient balance.')

        if not self.deduct_user_balance(user_data['id'], order.total_price,
                                        token):
            return self.set_order_failed(order, 'Failed to deduct balance.')

        return self.finalize_order(order, user_data, token)

    def is_item_available(self, order, token):
        item = request_item_detail(order.item_id, token)
        if not item or item.get('quantity', 0) < order.quantity_ordered:
            return False
        order.total_price = item.get('price', 0) * order.quantity_ordered
        return True

    def has_sufficient_balance(self, order, user_data):
        return float(user_data.get('balance', 0)) >= order.total_price

    def deduct_user_balance(self, user_id, amount, token):
        return request_balance_deduction(user_id, amount, token)

    def set_order_failed(self, order, message):
        order.status = Order.FAILED
        order.save()
        return Response({'status': FAILED, 'message': message})

    def finalize_order(self, order, user_data, token):
        order.status = Order.CONFIRMED
        adjust_inventory.delay(order.id, token)
        send_email.delay(user_data['email'], user_data['username'], order.id,
                         order.status)

        return Response(
            {'status': SUCCESS, 'message': 'Order created successfully.'})
