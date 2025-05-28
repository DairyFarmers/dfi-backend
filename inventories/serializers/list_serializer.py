from inventories.models import InventoryItem
from .base_serializer import InventoryItemBaseSerializer

class InventoryItemListSerializer(InventoryItemBaseSerializer):
    """
    Serializer for listing inventory items with basic fields.
    """
    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'dairy_type',
            'quantity', 'unit', 'price', 'expiry_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_active'] 