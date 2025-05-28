from rest_framework import serializers
from inventories.models import InventoryItem
from suppliers.serializers import SupplierDetailSerializer
from .base_serializer import InventoryItemBaseSerializer

class InventoryItemDetailSerializer(InventoryItemBaseSerializer):
    """
    Detailed serializer for inventory items with all fields and computed properties.
    """
    supplier_details = SupplierDetailSerializer(source='supplier', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)
    is_temperature_alert = serializers.BooleanField(read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'dairy_type', 'batch_number',
            'quantity', 'unit', 'price', 'storage_condition',
            'current_temperature', 'optimal_temperature_min',
            'optimal_temperature_max', 'manufacturing_date', 'expiry_date',
            'supplier', 'supplier_details', 'reorder_point',
            'minimum_order_quantity', 'is_low_stock', 'days_until_expiry',
            'is_temperature_alert', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_active'] 