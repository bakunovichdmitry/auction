from django.contrib import admin
from django.utils.html import format_html

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.photo.url}" width="100px" height="100px" />')

    list_display = (
        'image_tag',
        'title',
        'short_description'
    )
    search_fields = ['title']
