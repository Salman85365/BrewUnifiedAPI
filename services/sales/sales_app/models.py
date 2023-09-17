# models.py
from django.db import models


class Sale(models.Model):
    item = models.CharField(max_length=100)
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} - {self.quantity_sold} units"


class Order(models.Model):
    item_id = models.PositiveIntegerField()
    item_name = models.CharField(max_length=200)
    quantity_ordered = models.PositiveIntegerField(default=1)
