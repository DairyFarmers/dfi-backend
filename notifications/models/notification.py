from django.db import models
import uuid

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('expiry', 'Product Expiry'),
        ('low_stock', 'Low Stock'),
        ('price_change', 'Price Change'),
        ('order_status', 'Order Status'),
        ('payment_due', 'Payment Due'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_email = models.BooleanField(default=False)
    related_object_id = models.UUIDField(null=True)
    related_object_type = models.CharField(max_length=50, null=True)