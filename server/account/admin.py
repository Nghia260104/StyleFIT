from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'password', 'verified', 'profile_name', 'profile_photo', 'phone', 'address', 'role', 'created_at')
    list_filter = ('role', 'verified')
    search_fields = ('username', 'email', 'profile_name', 'phone')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Auth', {"fields": ("username", 'email', "password", "verified")}),
        ('Profile information', {"fields": ('profile_name', 'phone', 'address', 'created_at', 'role')})
    )
    add_fieldsets = (
        ('Auth', {"fields": ("username", 'email', "password", "verified")}),
        ('Profile information', {"fields": ('profile_name', 'phone', 'address', 'created_at', 'role')})
    )