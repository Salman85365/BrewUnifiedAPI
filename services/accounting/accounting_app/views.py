from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Transaction, Account
from rest_framework_simplejwt.views import TokenVerifyView
from .serializers import CustomUserSerializer, TransactionSerializer, AccountSerializer, CustomTokenVerifySerializer
from .permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):

        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer