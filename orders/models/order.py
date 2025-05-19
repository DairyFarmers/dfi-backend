from django.db import models
from django.core.validators import MinValueValidator
from .base_model import BaseModel
from inventories.models import InventoryItem
from suppliers.models import Supplier

class Order(BaseModel):
    """
    Model for managing dairy product orders.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned')
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]

    # Order Details
    order_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    
    # Customer Information
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=50)
    shipping_address = models.TextField()
    billing_address = models.TextField()

    # Order Status and Priority
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='draft'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    # Financial Information
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    shipping_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)
    tracking_number = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer_name']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['order_date'])
        ]

    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"

    def calculate_total(self):
        """Calculate the total amount including tax and shipping"""
        self.total_amount = self.subtotal + self.tax + self.shipping_cost
        self.save()

    def can_cancel(self):
        """Check if the order can be cancelled"""
        return self.status in ['draft', 'pending', 'confirmed']

    def can_modify(self):
        """Check if the order can be modified"""
        return self.status in ['draft', 'pending']

    def is_completed(self):
        """Check if the order is completed"""
        return self.status == 'delivered'

    def is_overdue(self):
        """Check if the order is overdue"""
        from django.utils import timezone
        if self.expected_delivery_date and self.status not in ['delivered', 'cancelled']:
            return self.expected_delivery_date < timezone.now().date()
        return False