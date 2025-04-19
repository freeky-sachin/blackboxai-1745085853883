import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import agencies.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rescue_agency_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            agencies.routing.websocket_urlpatterns
        )
    ),
})
