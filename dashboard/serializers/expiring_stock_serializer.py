from rest_framework import serializers
from inventories.models.inventory_item import InventoryItem

class ExpiringStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ["id", "name", "quantity", "expiry_date"]