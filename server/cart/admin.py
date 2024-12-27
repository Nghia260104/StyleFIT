from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'quantity')
    search_fields = ('buyer__username', 'product__name')