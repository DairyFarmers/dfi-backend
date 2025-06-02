from django.db import models
import uuid
from django.urls import reverse

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('expiry', 'Product Expiry'),
        ('low_stock', 'Low Stock'),
        ('price_change', 'Price Change'),
        ('order_status', 'Order Status'),
        ('payment_due', 'Payment Due'),
        ('system', 'System'),
    )

    PRIORITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    OBJECT_TYPES = (
        ('inventory_item', 'Inventory Item'),
        ('order', 'Order'),
        ('payment', 'Payment'),
        ('price', 'Price'),
        ('system', 'System'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    notification_title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_email = models.BooleanField(default=False)
    related_object_id = models.UUIDField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, choices=OBJECT_TYPES, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['read', 'user']),
            models.Index(fields=['notification_type', 'user']),
        ]

    def get_redirect_url(self):
        """Generate redirect URL based on notification type and related object"""
        if not self.related_object_id or not self.related_object_type:
            return None

        url_mapping = {
            'inventory_item': f'/inventory/items/{self.related_object_id}',
            'order': f'/orders/{self.related_object_id}',
            'payment': f'/payments/{self.related_object_id}',
            'price': f'/pricing/{self.related_object_id}',
        }

        return url_mapping.get(self.related_object_type)

    def mark_as_read(self):
        """Mark notification as read and save"""
        from django.utils import timezone
        self.read = True
        self.read_at = timezone.now()
        self.save(update_fields=['read', 'read_at', 'updated_at'])

    def __str__(self):
        return f"{self.notification_type} - {self.notification_title} ({self.user.email})"