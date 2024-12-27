from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'percentage', 'season', 'limit', 'used_number')
    list_filter = ('season',)
    search_fields = ('name', 'description', 'seller__username')
    readonly_fields = ('year',)