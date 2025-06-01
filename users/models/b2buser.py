from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class B2BUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=50, unique=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.IntegerField(default=30)  # days
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    account_manager = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='managed_b2b_accounts'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='b2b_users',
        related_query_name='b2b_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='b2b_users',
        related_query_name='b2b_user',
    )

    class Meta:
        db_table = 'b2b_users'
        ordering = ['-date_joined']