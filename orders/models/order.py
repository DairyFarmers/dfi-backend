from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        "pending",
        "processing",
        "shipped",
        "delivereded",
        "cancelleded",
    ]

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[(r, r) for r in STATUS_CHOICES], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"