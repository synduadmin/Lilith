from django.contrib import admin
from .models import Asset, AssetProvider
from django.utils.html import format_html

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('display_image','asset_type', 'prompt', 'user', 'created_at')
    list_filter = ('asset_type', 'created_at')
    search_fields = ('asset_type', 'prompt', 'user__username')
    date_hierarchy = 'created_at'

    def display_image(self, obj):
        return format_html('<img src="{}" width="120" height="120" />', obj.file.url)

@admin.register(AssetProvider)
class AssetProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

