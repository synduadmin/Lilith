from django.contrib import admin

# Register your models here.
# register logger
from .models import LogRecord
admin.site.register(LogRecord)
