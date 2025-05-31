from django.db import models
from .base_model import BaseModel
from .sale import Sale
from django.db.models import Sum

class Payment(BaseModel):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]

    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.id} for {self.sale.invoice_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update sale payment status
        total_paid = self.sale.payments.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        if total_paid >= self.sale.total_amount:
            self.sale.payment_status = 'paid'
        elif total_paid > 0:
            self.sale.payment_status = 'partial'
        else:
            self.sale.payment_status = 'pending'
        
        self.sale.save()