from django.contrib import admin
from .models import Configuration, ChatSession, ChatMessage, Sentence, Token

class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'temperature', 'max_tokens', 'top_p', 'top_k', 'frequency_penalty', 'presence_penalty', 'stop', 'default_depth')
    search_fields = ['name', 'model', 'prime']

admin.site.register(Configuration, ConfigurationAdmin)

class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'id', 'author', 'session_name', 'timestamp')
    search_fields = ['author', 'session_name']

admin.site.register(ChatSession, ChatSessionAdmin)

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'author', 'message', 'timestamp','json')
    search_fields = ['author', 'message']


admin.site.register(ChatMessage, ChatMessageAdmin)

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('role','chat_message_id','sentence', 'sentiment', 'position')
    search_fields = ['sentence','role','sentiment']

admin.site.register(Sentence, SentenceAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('position','token','pos','dep','entity')
    search_fields = ['position','token','pos','dep','entity']

admin.site.register(Token, TokenAdmin)
