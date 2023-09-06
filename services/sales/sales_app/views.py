from django.core.cache import cache
from .models import Sale, Order
from .serializers import SaleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import adjust_inventory
from django.http import JsonResponse

class SaleListCreate(APIView):

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Invalidate the warehouse cache when a sale happens
            cache.set("items_key", None, version=2)  # incrementing version to 2

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreate(APIView):
    def post(self, request):
        item_id = request.POST.get('item_id')
        item_name = request.POST.get('item_name')
        quantity_ordered = request.POST.get('quantity_ordered', 1)

        order = Order(item_name=item_name, quantity_ordered=quantity_ordered, item_id=item_id)
        order.save()

        # Trigger the Celery task to adjust inventory in warehouse service
        adjust_inventory.delay(order.id)

        return JsonResponse({'status': 'success', 'message': 'Order created successfully.'})
