from django.core.cache import cache
from .models import Sale
from .serializers import SaleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class SaleListCreate(APIView):

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Invalidate the warehouse cache when a sale happens
            cache.set("items_key", None, version=2)  # incrementing version to 2

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
