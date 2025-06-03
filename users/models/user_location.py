from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class UserLocation(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='locations'
    )
    location_type = models.CharField(
        max_length=20,
        choices=[
            ('home', 'Home'),
            ('work', 'Work'),
            ('farm', 'Farm'),
            ('storage', 'Storage'),
            ('other', 'Other')
        ]
    )
    is_primary = models.BooleanField(default=False)
    address_line1 = models.CharField(
        max_length=255,
        verbose_name=_("Address Line 1")
    )
    address_line2 = models.CharField(
        max_length=255,
        verbose_name=_("Address Line 2"),
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City")
    )
    state = models.CharField(
        max_length=100,
        verbose_name=_("State")
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name=_("Postal Code")
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        default="Sri Lanka"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Location")
        verbose_name_plural = _("User Locations")
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.user.email}'s {self.location_type} location"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other locations of this user to non-primary
            UserLocation.objects.filter(
                user=self.user,
                is_primary=True
            ).update(is_primary=False)
        super().save(*args, **kwargs)