from rest_framework import serializers
from orders.models.order import Order

class OrderAddSerializer(serializers.ModelSerializer):
    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero.")
        return value

    class Meta:
        model = Order
        fields = [
            'customer_name', 
            'customer_email', 
            'total_amount', 
            'order_status', 
            'order_date', 
            'delivery_date', 
            'notes'
        ]
        read_only_fields = ['order_date']

        # extra_kwargs = {
        #     'notes': {'required': False},
        #     'delivery_date': {'required': False},
        # }