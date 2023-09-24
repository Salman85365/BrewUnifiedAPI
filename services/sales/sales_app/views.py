from django.core.cache import cache
from .models import Sale, Order
from .serializers import SaleSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import adjust_inventory
from rest_framework import status


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


class OrderCreate(APIView):
    def get(self, request):
        return get_or_set_cache("orders_key", Order, OrderSerializer)

    def post(self, request):
        user_email = request.user_data['email']
        user_name = request.user_data['username']
        token = request.META.get("HTTP_AUTHORIZATION")

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(status=Order.PENDING)
            # TODO:make a function "request_balance_deduction" to
            #  Call the accounting service to get the account balance
            #  and check if the user has enough balance to place the order
            #  If the user has enough balance, create transaction which will
            #  update the account balance
            order.status = Order.CONFIRMED
            cache.delete("orders_key")
            adjust_inventory.delay(order.id, user_email, user_name, token)
            return Response({
                                'status': 'success',
                                'message': 'Order created successfully.'})
        return Response({'error': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
