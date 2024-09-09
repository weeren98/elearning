"""
ASGI config for elearning project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elearning.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Use Django's ASGI application to handle traditional HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns  # Add WebSocket routing
        )
    ),
})