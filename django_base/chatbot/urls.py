from django.urls import path
from .views import chatbot

app_name = 'chatbot'

urlpatterns = [
    path('', chatbot.as_view(), name='chatbot'),
]
