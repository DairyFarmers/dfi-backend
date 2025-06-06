from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from exceptions.exceptions import (
    InvalidCredentialsException, 
    InvalidDataException
)
from notifications.tasks import send_welcome_notification
from django.utils import timezone

class LoginService:        
    def login_user(self, request, email, password):
        user = authenticate(
            request, 
            email=email, 
            password=password
        )

        if not user:
            raise AuthenticationFailed("Invalid email or password")
        
        if not user.last_login:
            send_welcome_notification.delay(user.id)
                
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        tokens = user.tokens()
        
        role_data = {
            'id': str(user.role.id),
            'name': user.role.name,
            'permissions': user.role.get_all_permissions()
        } if user.role else None
        
        return {
            'email': user.email,
            'id': user.id,
            'full_name': user.get_full_name,
            'is_verified': user.is_verified,
            'role': role_data,
            'access_token': str(tokens['access_token']),
            'refresh_token': str(tokens['refresh_token'])
        }
        