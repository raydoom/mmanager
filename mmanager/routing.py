# coding=utf8

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from app.supervisor.consumer import ProcessLogConsumer
from app.docker.consumer import ContainerLogConsumer
from app.docker.consumer import ContainerConsoleConsumer
from django.urls import path,re_path
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    path(r"ws/supervisor/process_log", ProcessLogConsumer.as_asgi()),
    path(r"ws/docker/container_log", ContainerLogConsumer.as_asgi()),
    path(r"ws/docker/container_console", ContainerConsoleConsumer.as_asgi()),

]

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})