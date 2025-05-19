from rest_framework import serializers
from orders.models import Order, OrderItem
from .base_serializer import OrderBaseSerializer, OrderItemBaseSerializer

class OrderItemCreateUpdateSerializer(OrderItemBaseSerializer):
    """
    Serializer for creating and updating order items.
    """
    class Meta:
        model = OrderItem
        fields = [
            'inventory_item', 'quantity', 'unit_price',
            'discount', 'notes'
        ]

    def validate(self, data):
        """
        Validate inventory item stock availability.
        """
        inventory_item = data.get('inventory_item')
        quantity = data.get('quantity', 0)
        
        if inventory_item and quantity:
            if quantity > inventory_item.current_stock:
                raise serializers.ValidationError({
                    "quantity": f"Not enough stock. Available: {inventory_item.current_stock}"
                })
        return data

class OrderCreateUpdateSerializer(OrderBaseSerializer):
    """
    Serializer for creating and updating orders.
    """
    items = OrderItemCreateUpdateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'order_number', 'expected_delivery_date',
            'customer_name', 'customer_email', 'customer_phone',
            'shipping_address', 'billing_address', 'status',
            'priority', 'subtotal', 'tax', 'shipping_cost',
            'payment_status', 'payment_date', 'notes',
            'internal_notes', 'tracking_number', 'items'
        ]

    def create(self, validated_data):
        """
        Create order with nested items.
        """
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        order.calculate_total()
        return order

    def update(self, instance, validated_data):
        """
        Update order with nested items.
        """
        items_data = validated_data.pop('items', None)
        
        # Update order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if items_data is not None:
            # Remove existing items
            instance.items.all().delete()
            
            # Create new items
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        
        instance.calculate_total()
        instance.save()
        return instance

    def validate(self, data):
        """
        Validate order data.
        """
        # Validate status transitions
        if self.instance and 'status' in data:
            old_status = self.instance.status
            new_status = data['status']
            
            valid_transitions = {
                'draft': ['pending', 'cancelled'],
                'pending': ['confirmed', 'cancelled'],
                'confirmed': ['processing', 'cancelled'],
                'processing': ['shipped', 'cancelled'],
                'shipped': ['delivered', 'returned'],
                'delivered': ['returned'],
                'returned': [],
                'cancelled': []
            }
            
            if new_status not in valid_transitions.get(old_status, []):
                raise serializers.ValidationError({
                    "status": f"Invalid status transition from {old_status} to {new_status}"
                })
        
        return super().validate(data) 