import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

import django
django.setup()

import uvicorn

from django.conf import settings
from django.urls import include, path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat_asgi.routing import websocket_urlpatterns

# load environment
from dotenv import load_dotenv

load_dotenv()

print(f'environment {os.getenv("ENVIRONMENT")}')

# Initialize the Django ASGI application
django_asgi_app = get_asgi_application()

# Define the ASGI application for development
dev_application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

# Define the Uvicorn ASGI application
uvicorn_asgi_app = get_asgi_application()

# Define the Uvicorn configuration
uvicorn_config = uvicorn.Config(
    app=uvicorn_asgi_app,
    host="0.0.0.0",
    port=int(os.getenv("PORT", 8000)),
    log_level="info",
)

# Define the ASGI application
asgi_application = ProtocolTypeRouter({
    "http": uvicorn_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

# Determine which application to use based on the environment
if os.getenv("ENVIRONMENT") == "production":
    application = asgi_application
else:
    application = dev_application
