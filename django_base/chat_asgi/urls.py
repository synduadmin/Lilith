# chat/urls.py
from django.urls import path, re_path
from . import views
from .consumers import ChatConsumer

urlpatterns = [
    path("", views.index, name="chat_asgi_index"),
    path("<str:room_name>/", views.room, name="room"),
]