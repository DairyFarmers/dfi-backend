from rest_framework import serializers
from orders.models import Order, OrderItem
from .base_serializer import OrderBaseSerializer, OrderItemBaseSerializer
from inventories.serializers import InventoryItemListSerializer

class OrderItemDetailSerializer(OrderItemBaseSerializer):
    """
    Serializer for detailed order item information.
    """
    inventory_item = InventoryItemListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'inventory_item', 'quantity', 'unit_price',
            'discount', 'total_price', 'notes', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total_price', 'created_at', 'updated_at', 'is_active']

class OrderDetailSerializer(OrderBaseSerializer):
    """
    Serializer for detailed order information.
    """
    items = OrderItemDetailSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'order_date', 'expected_delivery_date',
            'actual_delivery_date', 'customer_name', 'customer_email',
            'customer_phone', 'shipping_address', 'billing_address',
            'status', 'status_display', 'priority', 'priority_display',
            'subtotal', 'tax', 'shipping_cost', 'total_amount',
            'payment_status', 'payment_status_display', 'payment_date',
            'notes', 'internal_notes', 'tracking_number', 'items',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'order_date', 'total_amount', 'created_at',
            'updated_at', 'is_active'
        ] 