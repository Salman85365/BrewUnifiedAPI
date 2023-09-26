from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import WarehouseItem
from .serializers import WarehouseItemSerializer


class WarehouseItemViewSet(
    viewsets.ReadOnlyModelViewSet):  # By default, allows only read
    # operations (list and retrieve)
    queryset = WarehouseItem.objects.all()
    serializer_class = WarehouseItemSerializer

    @action(detail=False, methods=['POST'], url_path='add-item')
    def add_item(self, request):
        if not request.user_data['role'] == 'Admin':
            return Response({'detail': 'Only administrators can add items.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseItemPrice(APIView):
    def put(self, request, item_id):
        if not request.user_data['role'] == 'Admin':
            return Response(
                {'detail': 'Only administrators can update item price.'},
                status=status.HTTP_403_FORBIDDEN)
        item = WarehouseItem.objects.get(id=item_id)
        serializer = WarehouseItemSerializer(item, data=request.data,
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseItemBuy(APIView):
    def post(self, request, item_id):
        item = WarehouseItem.objects.get(id=item_id)
        ordered_quantity = int(request.data.get('ordered_quantity'))
        if item.quantity >= ordered_quantity:
            item.quantity -= ordered_quantity
            item.save()
            return Response(
                {'message': f'Successfully bought {ordered_quantity} items'},
                status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Insufficient quantity available'},
                            status=status.HTTP_400_BAD_REQUEST)
