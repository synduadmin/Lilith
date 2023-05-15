from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'upload_date')
    readonly_fields = ('upload_date',)
    search_fields = ('file',)
