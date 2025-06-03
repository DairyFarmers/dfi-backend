from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from users.managers.user import UserManager
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from users.models.user_role import UserRole

AUTH_PROVIDERS = {'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=255, verbose_name=_("Email Address"), unique=True
    )
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, related_name='users')
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    
    @property
    def primary_location(self):
        return self.locations.filter(is_primary=True).first()

    @property
    def contact_info(self):
        return self.contact if hasattr(self, 'contact') else None

    def get_locations_by_type(self, location_type):
        return self.locations.filter(
            location_type=location_type,
            is_active=True
        )

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token)
        }
    
    def has_permission(self, permission_name):
        return self.role.permissions.get(permission_name, False) if self.role else False
    
