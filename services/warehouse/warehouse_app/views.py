from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WarehouseItem
from .serializers import WarehouseItemSerializer
from faker import Faker

fake = Faker()
class WarehouseItemList(APIView):
    def get(self, request):
        items = WarehouseItem.objects.all()
        serializer = WarehouseItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WarehouseItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WarehouseItemPrice(APIView):
    def put(self, request, item_id):
        item = WarehouseItem.objects.get(id=item_id)
        serializer = WarehouseItemSerializer(item, data=request.data, partial=True)
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
            return Response({'message': f'Successfully bought {ordered_quantity} items'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Insufficient quantity available'}, status=status.HTTP_400_BAD_REQUEST)

def random_float(min_val, max_val, decimals=2):
    return fake.random_int(min_val * (10 ** decimals), max_val * (10 ** decimals)) / (10 ** decimals)
class CreateDummyDataWarehouse(APIView):
    def get(self, request):
        # Generate fake data for WarehouseItem model
        name = fake.unique.first_name()
        description = fake.sentence(nb_words=10)
        quantity = fake.random_int(min=1, max=1000)
        price = random_float(1, 1000)

        # Create a new WarehouseItem instance and save to database
        item = WarehouseItem(
            name=name,
            description=description,
            quantity=quantity,
            price=price
        )
        item.save()
        return Response({'message': 'Successfully created a new WarehouseItem instance'}, status=status.HTTP_201_CREATED)


