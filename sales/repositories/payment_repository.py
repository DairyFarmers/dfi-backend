from django.db import transaction
from django.db.models import Sum, Count
from sales.models import Payment

class PaymentRepository:
    def __init__(self):
        self.model = Payment

    def get_all_payments(self, filters=None):
        """
        Get all active payments with optional filters
        """
        queryset = self.model.objects.filter(is_active=True)
        if filters:
            queryset = queryset.filter(**filters)
        return queryset.select_related('sale', 'created_by')

    def get_payment_by_id(self, payment_id):
        """
        Get specific payment by ID
        """
        return (self.model.objects
                .filter(id=payment_id, is_active=True)
                .select_related('sale', 'created_by')
                .first())

    def get_sale_payments(self, sale_id):
        """
        Get all payments for a specific sale
        """
        return (self.model.objects
                .filter(sale_id=sale_id, is_active=True)
                .select_related('sale')
                .order_by('-payment_date'))

    @transaction.atomic
    def create_payment(self, payment_data, user):
        """
        Create a new payment with user tracking
        """
        payment = self.model(
            **payment_data,
            created_by=user,
            updated_by=user
        )
        payment.save()
        return payment

    @transaction.atomic
    def update_payment(self, payment_id, payment_data, user):
        """
        Update existing payment
        """
        payment = self.get_payment_by_id(payment_id)
        if payment:
            for key, value in payment_data.items():
                setattr(payment, key, value)
            payment.updated_by = user
            payment.save()
        return payment

    @transaction.atomic
    def delete_payment(self, payment_id, user):
        """
        Soft delete a payment
        """
        payment = self.get_payment_by_id(payment_id)
        if payment:
            payment.soft_delete(user=user)
            return True
        return False

    def get_payment_stats(self, sale_id):
        """
        Get payment statistics for a sale
        """
        return self.model.objects.filter(
            sale_id=sale_id,
            is_active=True
        ).aggregate(
            total_paid=Sum('amount'),
            payment_count=Count('id'),
            last_payment_date=Max('payment_date')
        )

    def get_payment_methods_summary(self, sale_id):
        """
        Get summary of payments by payment method
        """
        return (self.model.objects
                .filter(sale_id=sale_id, is_active=True)
                .values('payment_method')
                .annotate(
                    total_amount=Sum('amount'),
                    count=Count('id')
                ))

    def check_duplicate_payment(self, reference_number):
        """
        Check for duplicate payment reference numbers
        """
        return self.model.objects.filter(
            reference_number=reference_number,
            is_active=True
        ).exists()