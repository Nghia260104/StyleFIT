from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('account', 'type', 'content_preview','created_at', 'read', 'partner')
    list_filter = ('type', 'read')
    search_fields = ('account__email', 'content')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        # Show only the first 50 characters of the content
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'