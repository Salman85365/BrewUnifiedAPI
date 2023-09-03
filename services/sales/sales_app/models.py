# models.py
from django.db import models

class Sale(models.Model):
    item = models.CharField(max_length=100)
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} - {self.quantity_sold} units"
