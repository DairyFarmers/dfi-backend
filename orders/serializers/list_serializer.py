from rest_framework import serializers
from orders.models import Order, OrderItem
from .base_serializer import OrderBaseSerializer, OrderItemBaseSerializer

class OrderItemListSerializer(OrderItemBaseSerializer):
    """
    Serializer for listing order items with basic information.
    """
    inventory_item_name = serializers.CharField(source='inventory_item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'inventory_item_name', 'quantity',
            'unit_price', 'total_price', 'is_active'
        ]
        read_only_fields = ['total_price', 'is_active']

class OrderListSerializer(OrderBaseSerializer):
    """
    Serializer for listing orders with basic information.
    """
    items_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name',
            'order_date', 'status', 'total_amount',
            'payment_status', 'items_count', 'is_active'
        ]
        read_only_fields = ['order_date', 'is_active'] 