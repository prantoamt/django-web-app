from django.contrib import admin
from .models import Order

class OrderInline(admin.TabularInline):
    model = Order

# Register your models here.
admin.site.register(Order)