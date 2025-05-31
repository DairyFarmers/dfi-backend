from rest_framework import serializers
from sales.models import Payment, Sale
from sales.serializers.sale_serializer import SaleSerializer
from django.db.models import Sum

class PaymentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed payment information including sale details
    """
    sale = SaleSerializer(read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'sale',
            'amount',
            'payment_date',
            'payment_method',
            'payment_method_display',
            'reference_number',
            'notes',
            'created_at',
            'created_by_name',
            'is_active'
        ]
        read_only_fields = ['created_at', 'created_by_name', 'is_active']

class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new payments
    """
    sale_id = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.filter(is_active=True),
        source='sale'
    )

    class Meta:
        model = Payment
        fields = [
            'sale_id',
            'amount',
            'payment_method',
            'payment_date',
            'reference_number',
            'notes'
        ]

    def validate(self, attrs):
        """
        Validate payment amount against sale remaining balance
        """
        sale = attrs['sale']
        amount = attrs['amount']

        # Calculate total amount paid so far
        total_paid = sale.payments.filter(is_active=True).aggregate(
            total=Sum('amount'))['total'] or 0
        
        remaining_balance = sale.total_amount - total_paid

        if amount > remaining_balance:
            raise serializers.ValidationError({
                'amount': f'Payment amount ({amount}) exceeds remaining balance ({remaining_balance})'
            })

        return attrs

class PaymentListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing payments
    """
    sale_invoice = serializers.CharField(source='sale.invoice_number', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'sale_invoice',
            'amount',
            'payment_date',
            'payment_method_display',
            'reference_number'
        ]