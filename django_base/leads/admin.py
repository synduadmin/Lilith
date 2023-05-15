# leads app, admin.py
from django.contrib import admin
from .models import Lead

class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'interested_as', 'created_at', 'updated_at', 'ip_address')

admin.site.register(Lead, LeadAdmin)
