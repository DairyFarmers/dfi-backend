from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class UserContact(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='contact'
    )
    phone_primary = models.CharField(
        max_length=15,
        verbose_name=_("Primary Phone"),
        null=True,
        blank=True
    )
    phone_secondary = models.CharField(
        max_length=15,
        verbose_name=_("Secondary Phone"),
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Contact")
        verbose_name_plural = _("User Contacts")

    def __str__(self):
        return f"{self.user.email}'s contact info"