from django.contrib import admin
from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price', 'quantity_in_stock', 'category', 'active')
    list_filter = ('category', 'active')
    search_fields = ('name', 'description', 'seller__email')

    readonly_fields = ('seller',)