from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'content_preview', 'buyer', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'buyer__username', 'content')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'