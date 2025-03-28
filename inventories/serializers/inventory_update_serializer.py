from rest_framework import serializers
from inventories.models.inventory_item import InventoryItem

class InventoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ["name", "description", "quantity", "price"]