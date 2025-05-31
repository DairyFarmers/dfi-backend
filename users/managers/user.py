from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
    
        email = self.normalize_email(email)
        self.validate_email(email)
    
        if not extra_fields.get('first_name'):
            raise ValueError(_('The first name field must be set'))
    
        if not extra_fields.get('last_name'):
            raise ValueError(_('The last name field must be set'))
        
        if not extra_fields.get('role'):
            extra_fields.setdefault('role', 'farmer')
    
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', "admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('Invalid email address'))
        return None

