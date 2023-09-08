from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Transaction, Account
from rest_framework_simplejwt.views import TokenVerifyView
from .serializers import CustomUserSerializer, TransactionSerializer, AccountSerializer, CustomTokenVerifySerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer