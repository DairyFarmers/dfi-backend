from rest_framework import serializers
from orders.models.order import Order

class OrderAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'total_price', 'status']