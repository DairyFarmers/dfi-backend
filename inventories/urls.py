# inventories URL Configuration

from django.contrib import admin
from django.urls import path
from inventories.views.inventory_list_view import InventoryListView
from inventories.views.inventory_detail_view import InventoryDetailView
from inventories.views.inventory_add_view import InventoryAddView

urlpatterns = [
    path('list', InventoryListView.as_view(), name='inventory-list'),
    path('item/<int:item_id>', InventoryDetailView.as_view(), name='inventory-detail'),
    path('add', InventoryAddView.as_view(), name='inventory-add'),
]
