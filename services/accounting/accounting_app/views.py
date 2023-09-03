# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Price
from .serializers import PriceSerializer

class PriceListCreate(APIView):
    def get(self, request):
        prices = Price.objects.all()
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriceDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Price, pk=pk)

    def get(self, request, pk):
        price = self.get_object(pk)
        serializer = PriceSerializer(price)
        return Response(serializer.data)

    def put(self, request, pk):
        price = self.get_object(pk)
        serializer = PriceSerializer(price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
