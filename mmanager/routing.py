
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from app.supervisor.consumer import ProcessLog
from django.urls import path,re_path
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    path(r"ws/supervisor/process_log", ProcessLog.as_asgi()),

]

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})