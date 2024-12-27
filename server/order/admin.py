from django.contrib import admin
from .models import Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'total_price', 'created_at', 'shipped_date')
    list_filter = ('status',)
    search_fields = ('buyer__username', 'id')
    readonly_fields = ('created_at',)