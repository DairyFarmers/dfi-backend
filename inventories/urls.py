# inventories URL Configuration

from django.urls import path
from inventories.views import (
    InventoryItemView,
    InventoryItemDetailView,
    InventoryItemTemperatureView
)

app_name = 'inventories'

urlpatterns = [
    path('items/', InventoryItemView.as_view(), name='inventory-items'),
    path('items/<int:pk>', InventoryItemDetailView.as_view(), name='inventory-item-detail'),
    path('items/<int:pk>/temperature/', InventoryItemTemperatureView.as_view(), name='inventory-item-temperature'),
]
