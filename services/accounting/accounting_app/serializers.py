from rest_framework import serializers
from .models import CustomUser, Transaction, Account
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_active']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class CustomTokenVerifySerializer(TokenVerifySerializer):
    @classmethod
    def validate(self, attrs):
        super().validate(self, attrs)
        token = UntypedToken(attrs["token"])
        user_id = token.get("user_id")

        if CustomUser.objects.filter(id=user_id).exists():
            user_details = CustomUserSerializer(CustomUser.objects.get(id=user_id)).data
            return {"data": user_details}
        else:
            raise serializers.ValidationError("This token is invalid or expired")