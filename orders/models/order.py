from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)  # Email is optional now
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Renamed to total_amount
    order_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )  # Renamed status to order_status
    order_date = models.DateTimeField(auto_now_add=True)  # Renamed created_at to order_date
    updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateField(null=True, blank=True)  # Optional delivery date field
    notes = models.TextField(blank=True, null=True)  # Optional notes for the order
    payment_status = models.CharField(
        max_length=20, choices=[("paid", "Paid"), ("unpaid", "Unpaid")], default="unpaid"
    )  # Added payment status

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

    class Meta:
        ordering = ['-order_date']  # Orders are sorted by most recent first by default