from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path('ws/chat/<int:receiver_id>/', ChatConsumer.as_asgi()),
]