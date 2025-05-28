from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 