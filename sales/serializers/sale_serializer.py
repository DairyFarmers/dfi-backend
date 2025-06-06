from rest_framework import serializers
from sales.models import Sale
from orders.serializers.detail_serializer import OrderDetailSerializer
from users.serializers.user_serializer import UserSerializer
from decimal import Decimal
import uuid

class SaleSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('invoice_number', 'sale_date', 'seller')

class SaleCreateSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(
        required=True,
        help_text="UUID of the order associated with this sale"
    )
    payment_status = serializers.ChoiceField(
        choices=['pending', 'partial', 'paid'],
        default='pending'
    )
    payment_due_date = serializers.DateField(required=True)
    tax_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        min_value=Decimal('0.00')
    )
    discount_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        min_value=Decimal('0.00')
    )
    shipping_cost = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('15.00'),
        min_value=Decimal('0.00')
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500
    )
    
    class Meta:
        model = Sale
        fields = [
            'order_id',
            'payment_status',
            'payment_due_date',
            'tax_amount',
            'discount_amount',
            'shipping_cost',
            'notes'
        ]

    def validate_order_id(self, value):
        from orders.models import Order
        try:
            order = Order.objects.get(id=value)
            if hasattr(order, 'sale'):
                raise serializers.ValidationError(
                    "A sale already exists for this order"
                )
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError(
                f"Order with id {value} does not exist"
            )

    def validate(self, data):
        """
        Validate the data before sale creation
        """
        # Ensure discount doesn't exceed reasonable limits
        if data.get('discount_amount', 0) > 0:
            from orders.models import Order
            order = Order.objects.get(id=data['order_id'])
            if data['discount_amount'] > order.total_amount:
                raise serializers.ValidationError(
                    "Discount amount cannot be greater than order total"
                )

        return data