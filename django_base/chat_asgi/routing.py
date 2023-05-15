from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"^chat_asgi/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
]
#ValueError: No route found for path 'chat_asgi/7f73ae7d-cb69-4129-a11c-d584e33d3512/'.
