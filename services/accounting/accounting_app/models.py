from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

class Transaction(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'
    TRANSACTION_TYPES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

class Account(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transactions = models.ManyToManyField(Transaction, related_name='accounts')
