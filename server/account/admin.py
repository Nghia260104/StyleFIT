from django.contrib import admin
from .models import Account

# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'profile_name', 'authentication_code', 'code_expired', 'profile_photo', 'phone', 'address', 'role', 'verified', 'created_at')
    list_filter = ('role', 'verified')
    search_fields = ('email', 'profile_name', 'phone')
    readonly_fields = ('created_at',)