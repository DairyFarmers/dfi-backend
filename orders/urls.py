# orders URL Configuration

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.order_views import OrderViewSet
from .views.order_item_views import OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
]
