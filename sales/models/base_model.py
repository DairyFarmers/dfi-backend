from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    """
    Abstract base model that provides common fields and functionality
    for all models in the sales module.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        null=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        null=True
    )
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        """
        Soft delete the record by setting is_active to False
        and recording deletion timestamp
        """
        self.is_active = False
        self.deleted_at = timezone.now()
        if user:
            self.updated_by = user
        self.save()

    def restore(self, user=None):
        """
        Restore a soft-deleted record
        """
        self.is_active = True
        self.deleted_at = None
        if user:
            self.updated_by = user
        self.save()

    def save(self, *args, **kwargs):
        """
        Override save method to handle user tracking
        """
        user = kwargs.pop('user', None)
        if user:
            if not self.pk:  # New instance
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)