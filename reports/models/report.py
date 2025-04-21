from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    REPORT_TYPES = [
        ("sales", "Sales Report"),
        ("inventory", "Inventory Report"),
        ("user_activity", "User Activity Report"),
    ]

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
    file_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.generated_at}"