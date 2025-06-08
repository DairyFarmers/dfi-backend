import uuid
from django.db import models
from django.conf import settings

class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('inventory', 'Inventory Report'),
        ('orders', 'Orders Report'),
        ('user_activity', 'User Activity Report'),
    ]

    FORMAT_TYPES = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=FORMAT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    file = models.FileField(upload_to='docs/', null=True, blank=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    filters = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['report_type', 'status']),
            models.Index(fields=['generated_at']),
        ]

    def __str__(self):
        return f"{self.report_type} Report - {self.generated_at.strftime('%Y-%m-%d %H:%M')}"