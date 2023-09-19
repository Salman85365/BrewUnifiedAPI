from django.core.cache import cache
from .models import Sale, Order
from .serializers import SaleSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import adjust_inventory
from django.http import JsonResponse
from rest_framework import status

class SaleListCreate(APIView):

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Invalidate the warehouse cache when a sale happens
            cache.set("items_key", None, version=2)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreate(APIView):
    def post(self, request):
        user_email = request.user_data['email']
        user_name = request.user_data['username']
        token = request.META.get("HTTP_AUTHORIZATION")
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            # Trigger the Celery task to adjust inventory in warehouse service
            adjust_inventory(order.id, user_email, user_name, token)
            return JsonResponse({'status': 'success', 'message': 'Order created successfully.'})
        return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


