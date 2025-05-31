import django_filters
from sales.models import Sale, Payment

class SaleFilter(django_filters.FilterSet):
    """
    Filter set for Sale model.
    """
    invoice_number = django_filters.CharFilter(lookup_expr='icontains')
    order_number = django_filters.CharFilter(field_name='order__order_number', lookup_expr='icontains')
    customer_name = django_filters.CharFilter(field_name='order__customer_name', lookup_expr='icontains')
    payment_status = django_filters.ChoiceFilter(choices=Sale.PAYMENT_STATUS_CHOICES)
    min_total = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_total = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    sale_date_after = django_filters.DateFilter(field_name='sale_date', lookup_expr='date__gte')
    sale_date_before = django_filters.DateFilter(field_name='sale_date', lookup_expr='date__lte')
    payment_due_after = django_filters.DateFilter(field_name='payment_due_date', lookup_expr='gte')
    payment_due_before = django_filters.DateFilter(field_name='payment_due_date', lookup_expr='lte')
    seller = django_filters.CharFilter(field_name='seller__username', lookup_expr='icontains')

    class Meta:
        model = Sale
        fields = [
            'invoice_number', 'order_number', 'customer_name',
            'payment_status', 'seller'
        ]

class PaymentFilter(django_filters.FilterSet):
    """
    Filter set for Payment model.
    """
    invoice_number = django_filters.CharFilter(field_name='sale__invoice_number', lookup_expr='icontains')
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    payment_date_after = django_filters.DateFilter(field_name='payment_date', lookup_expr='date__gte')
    payment_date_before = django_filters.DateFilter(field_name='payment_date', lookup_expr='date__lte')
    reference_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Payment
        fields = [
            'invoice_number', 'payment_method',
            'reference_number'
        ]