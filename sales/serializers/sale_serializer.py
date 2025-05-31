from rest_framework import serializers
from sales.models import Sale
from orders.serializers.detail_serializer import OrderDetailSerializer
from users.serializers.user_serializer import UserSerializer

class SaleSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('invoice_number', 'sale_date', 'seller')

class SaleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['payment_status', 'payment_due_date', 'tax_amount', 'discount_amount', 'notes']