from rest_framework import serializers

class OrderBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for Order model with common validation logic.
    """
    def validate_total_amount(self, value):
        """Validate total amount is positive"""
        if value and value < 0:
            raise serializers.ValidationError("Total amount cannot be negative")
        return value

    def validate(self, data):
        """Validate order dates"""
        if 'expected_delivery_date' in data and 'order_date' in data:
            if data['expected_delivery_date'] < data['order_date'].date():
                raise serializers.ValidationError({
                    "expected_delivery_date": "Expected delivery date cannot be earlier than order date"
                })
        return data

class OrderItemBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for OrderItem model with common validation logic.
    """
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value

    def validate_unit_price(self, value):
        """Validate unit price is not negative"""
        if value < 0:
            raise serializers.ValidationError("Unit price cannot be negative")
        return value 