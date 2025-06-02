from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .base_model import BaseModel
import uuid

class Supplier(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.contact_person})"

    class Meta:
        ordering = ['-rating', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['rating']),
        ] 