from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def create_user(
        self, 
        email, 
        first_name, 
        last_name, 
        password=None,
        role=2,
        **extra_fields
        ):
        if email:
            email = self.normalize_email(email)
            self.validate_email(email)
        else:
            raise ValueError(_('The email field must be set'))
        
        if not first_name:
            raise ValueError(_('The first name field must be set'))
        
        if not last_name:
            raise ValueError(_('The last name field must be set'))
        
        if not role:
            raise ValueError(_('The role field must be set'))
        
        user = self.model(
            email=email, 
            first_name=first_name, 
            last_name=last_name,
            role=role, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('Invalid email address'))
        return None

