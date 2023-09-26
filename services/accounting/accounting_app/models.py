from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    USER = 'User'
    ROLES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]
    role = models.CharField(max_length=50, choices=ROLES, default=USER)

    def __str__(self):
        return f"{self.username} - {self.id}"


class Transaction(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'
    TRANSACTION_TYPES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]
    description = models.CharField(max_length=255, null=True, blank=True)
    transaction_type = models.CharField(max_length=10,
                                        choices=TRANSACTION_TYPES)
    account = models.ForeignKey('Account', related_name='transactions',
                                on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.user} - {self.amount}"


class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} - {self.balance}"
