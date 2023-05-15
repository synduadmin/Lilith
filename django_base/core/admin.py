from django.contrib import admin
from .models import AIConfiguration, AIInteraction

class AIConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'temperature', 'max_tokens', 'top_p', 'top_k', 'frequency_penalty', 'presence_penalty', 'stop', 'default_depth')
    search_fields = ['name', 'model', 'prime']

admin.site.register(AIConfiguration, AIConfigurationAdmin)

class AIInteractionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'configuration_id', 'timestamp', 'user', 'role', 'output')
    list_filter = ('configuration_id', 'timestamp', 'user', 'role')
    search_fields = ('user__email', 'role', 'input', 'output')

admin.site.register(AIInteraction, AIInteractionsAdmin)
