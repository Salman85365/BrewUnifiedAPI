# models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
