from django.db.models import Sum, F, Q, Count
from django.db import transaction
from sales.models import Sale, Payment
from sales.filters import SaleFilter, PaymentFilter

class SaleRepository:
    def __init__(self):
        self.model = Sale
        self.payment_model = Payment

    def get_all_sales(self, filters=None):
        queryset = self.model.objects.filter(is_active=True)
        if filters:
            filterset = SaleFilter(filters, queryset=queryset)
            queryset = filterset.qs
        return queryset.select_related('order', 'seller')

    def get_sale_payments(self, sale_id, filters=None):
        queryset = self.payment_model.objects.filter(
            sale_id=sale_id, 
            is_active=True
        )
        if filters:
            filterset = PaymentFilter(filters, queryset=queryset)
            queryset = filterset.qs
        return queryset.select_related('sale')

    def get_sale_by_id(self, sale_id):
        return self.model.objects.filter(id=sale_id).first()

    def get_sale_by_invoice(self, invoice_number):
        return self.model.objects.filter(invoice_number=invoice_number).first()

    def get_sales_stats(self, filters=None):
        queryset = self.model.objects.filter(is_active=True)
        if filters:
            filterset = SaleFilter(filters, queryset=queryset)
            queryset = filterset.qs

        return queryset.aggregate(
            total_sales_count=Count('id'),
            total_amount=Sum('total_amount'),
            total_tax=Sum('tax_amount'),
            total_discount=Sum('discount_amount'),
            total_shipping=Sum('shipping_cost'),
            total_profit=Sum(
                F('total_amount') - F('discount_amount') - 
                F('tax_amount') - F('shipping_cost')
            )
        )
    
    @transaction.atomic
    def update_sale(self, sale_id, sale_data):
        sale = self.get_sale_by_id(sale_id)
        if sale:
            for key, value in sale_data.items():
                setattr(sale, key, value)
            sale.save()
        return sale

    def delete_sale(self, sale_id):
        sale = self.get_sale_by_id(sale_id)
        if sale:
            sale.delete()
            return True
        return False
    
    def create_sale(self, sale_data, user):
        sale = self.model(**sale_data)
        sale.created_by = user
        sale.updated_by = user
        sale.save()
        return sale