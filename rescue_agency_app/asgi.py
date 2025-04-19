import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import agencies.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rescue_agency_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        agencies.routing.websocket_urlpatterns
    ),
})
