from inventories.models import InventoryItem
from .base_serializer import InventoryItemBaseSerializer

class InventoryItemCreateUpdateSerializer(InventoryItemBaseSerializer):
    """
    Serializer for creating and updating inventory items with required fields.
    """
    class Meta:
        model = InventoryItem
        fields = [
            'name', 'description', 'dairy_type', 'batch_number',
            'quantity', 'unit', 'price', 'storage_condition',
            'optimal_temperature_min', 'optimal_temperature_max',
            'manufacturing_date', 'expiry_date', 'supplier',
            'reorder_point', 'minimum_order_quantity'
        ] 