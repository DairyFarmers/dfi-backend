from rest_framework import serializers
from orders.models import Order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status only."""
    
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """Validate status transitions."""
        instance = self.instance
        if not instance:
            return value

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

        if value not in valid_transitions.get(instance.status, []):
            raise serializers.ValidationError(
                f"Invalid status transition from '{instance.status}' to '{value}'"
            )

        return value