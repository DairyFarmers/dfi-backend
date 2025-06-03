import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class UserSettings(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    privacy_settings = models.JSONField(
        default=dict,
        help_text=_("Privacy and data sharing preferences")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('User Setting')
        verbose_name_plural = _('User Settings')

    def __str__(self):
        return f"{self.user.email}'s settings"

    def get_default_privacy_settings(self):
        return {
            "share_contact_info": False,
            "share_location": False,
            "share_inventory": False,
            "share_analytics": False,
            "allow_marketing": False
        }

    def initialize_defaults(self):
        """Initialize preference defaults if not set"""
        if not self.privacy_settings:
            self.privacy_settings = self.get_default_privacy_settings()
            
        self.save()