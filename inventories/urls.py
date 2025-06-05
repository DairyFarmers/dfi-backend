# inventories URL Configuration

from django.urls import path
from inventories.views import (
    InventoryItemView,
    InventoryItemDetailView,
    InventoryItemTemperatureView
)

urlpatterns = [
    path('items/', InventoryItemView.as_view(), name='inventory-items'),
    path('items/<uuid:pk>', InventoryItemDetailView.as_view(), name='inventory-item-detail'),
    path('items/<uuid:pk>/temperature/', InventoryItemTemperatureView.as_view(), name='inventory-item-temperature'),
]
