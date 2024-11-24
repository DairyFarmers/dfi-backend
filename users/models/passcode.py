from django.db import models
from users.models.user import User
import uuid
from django.utils import timezone
from datetime import timedelta

class Passcode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passcode = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(minutes=5)
        super().save(*args, **kwargs)