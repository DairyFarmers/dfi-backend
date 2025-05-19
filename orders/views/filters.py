import django_filters
from orders.models import Order, OrderItem

class OrderFilter(django_filters.FilterSet):
    """
    Filter set for Order model.
    """
    order_number = django_filters.CharFilter(lookup_expr='icontains')
    customer_name = django_filters.CharFilter(lookup_expr='icontains')
    customer_email = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    payment_status = django_filters.ChoiceFilter(choices=Order.PAYMENT_STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Order.PRIORITY_CHOICES)
    min_total = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_total = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date_after = django_filters.DateFilter(field_name='order_date', lookup_expr='date__gte')
    order_date_before = django_filters.DateFilter(field_name='order_date', lookup_expr='date__lte')
    expected_delivery_after = django_filters.DateFilter(field_name='expected_delivery_date', lookup_expr='gte')
    expected_delivery_before = django_filters.DateFilter(field_name='expected_delivery_date', lookup_expr='lte')

    class Meta:
        model = Order
        fields = [
            'order_number', 'customer_name', 'customer_email',
            'status', 'payment_status', 'priority'
        ]

class OrderItemFilter(django_filters.FilterSet):
    """
    Filter set for OrderItem model.
    """
    order_number = django_filters.CharFilter(field_name='order__order_number', lookup_expr='icontains')
    inventory_item_name = django_filters.CharFilter(field_name='inventory_item__name', lookup_expr='icontains')
    min_quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    min_unit_price = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    max_unit_price = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    has_discount = django_filters.BooleanFilter(field_name='discount', lookup_expr='gt', exclude=True)
    order_status = django_filters.ChoiceFilter(
        field_name='order__status',
        choices=Order.STATUS_CHOICES
    )

    class Meta:
        model = OrderItem
        fields = [
            'order_number', 'inventory_item_name',
            'min_quantity', 'max_quantity',
            'min_unit_price', 'max_unit_price',
            'has_discount', 'order_status'
        ] 