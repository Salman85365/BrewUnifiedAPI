from django.contrib import admin
from .models import CustomUser, Transaction, Account
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(Account)
