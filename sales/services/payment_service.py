from django.db import transaction
from django.utils import timezone
from django.db.models import Sum
from sales.repositories.payment_repository import PaymentRepository
from sales.repositories.sale_repository import SaleRepository

class PaymentService:
    def __init__(self):
        self.payment_repository = PaymentRepository()
        self.sale_repository = SaleRepository()

    @transaction.atomic
    def create_payment(self, sale_id, payment_data, user):
        """
        Create a new payment and update sale payment status
        """
        # Get sale and validate
        sale = self.sale_repository.get_sale_by_id(sale_id)
        if not sale:
            raise ValueError("Sale not found")

        # Calculate remaining balance
        total_paid = sale.payments.filter(is_active=True).aggregate(
            total=Sum('amount'))['total'] or 0
        remaining = sale.total_amount - total_paid

        # Validate payment amount
        amount = payment_data.get('amount', 0)
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")
        if amount > remaining:
            raise ValueError(f"Payment amount ({amount}) exceeds remaining balance ({remaining})")

        # Create payment
        payment = self.payment_repository.create_payment({
            'sale': sale,
            'amount': amount,
            'payment_method': payment_data.get('payment_method'),
            'payment_date': payment_data.get('payment_date', timezone.now()),
            'reference_number': payment_data.get('reference_number'),
            'notes': payment_data.get('notes'),
        }, user)

        # Update sale payment status
        self._update_sale_payment_status(sale)

        return payment

    @transaction.atomic
    def void_payment(self, payment_id, user):
        """
        Void a payment and update sale payment status
        """
        payment = self.payment_repository.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        if not payment.is_active:
            raise ValueError("Payment already voided")

        # Soft delete the payment
        self.payment_repository.delete_payment(payment_id, user)

        # Update sale payment status
        self._update_sale_payment_status(payment.sale)

        return payment

    def get_payment_summary(self, sale_id):
        """
        Get payment summary for a sale
        """
        sale = self.sale_repository.get_sale_by_id(sale_id)
        if not sale:
            raise ValueError("Sale not found")

        payments = self.payment_repository.get_sale_payments(sale_id)
        total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
        remaining = sale.total_amount - total_paid

        return {
            'sale_id': sale_id,
            'invoice_number': sale.invoice_number,
            'total_amount': sale.total_amount,
            'total_paid': total_paid,
            'remaining_balance': remaining,
            'payment_status': sale.payment_status,
            'payment_count': payments.count(),
            'last_payment_date': payments.order_by('-payment_date').values_first('payment_date')
        }

    def _update_sale_payment_status(self, sale):
        """
        Update sale payment status based on payments
        """
        total_paid = sale.payments.filter(is_active=True).aggregate(
            total=Sum('amount'))['total'] or 0

        if total_paid >= sale.total_amount:
            status = 'paid'
        elif total_paid > 0:
            status = 'partial'
        else:
            status = 'pending'

        self.sale_repository.update_sale(
            sale.id, 
            sale_data={
                'payment_status': status,
                'updated_by': sale.updated_by
            }
        )