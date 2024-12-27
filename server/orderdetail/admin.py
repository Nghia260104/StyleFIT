from django.contrib import admin
from .models import OrderDetail

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')