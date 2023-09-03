# models.py
from django.db import models

class Price(models.Model):
    item = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Assuming a maximum price of 999999.99

    def __str__(self):
        return f"{self.item} - ${self.price}"
