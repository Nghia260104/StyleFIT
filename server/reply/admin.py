from django.contrib import admin
from .models import Reply

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('review', 'content_preview', 'seller', 'created_at')
    search_fields = ('seller__email', 'content', 'review__product__name')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'