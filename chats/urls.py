from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views.chat_view import ChatViewSet

router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]