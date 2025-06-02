from django.db import models
from .base_model import BaseModel
from orders.models import Order
from django.db.models import Sum
import uuid

class Sale(BaseModel):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled')
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    order = models.OneToOneField(
        Order, 
        on_delete=models.PROTECT,
        related_name='sale'
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    sale_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_due_date = models.DateField(null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    seller = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='sales'
    )

    def calculate_total(self):
        """Calculate total amount including tax, shipping, and discounts"""
        subtotal = self.order.total_amount
        total = subtotal + self.tax_amount + self.shipping_cost - self.discount_amount
        return total

    def update_payment_status(self):
        """Update payment status based on payments received"""
        total_paid = self.payments.filter(is_active=True).aggregate(
            total=Sum('amount')
        )['total'] or 0

        if total_paid >= self.total_amount:
            self.payment_status = 'paid'
        elif total_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'
        self.save()