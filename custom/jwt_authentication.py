from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import jwt

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']) or None
        else:
            access_token = self.get_raw_token(header)
        
        validated_token = self.validate_token(access_token, settings.SIMPLE_JWT['SIGNING_KEY'])
        if validated_token is False:
            return None
        elif validated_token is True:      
            if refresh_token:
                try:
                    new_access_token = self.refresh_access_token(refresh_token)    
                    validated_token = self.get_validated_token(new_access_token)
                    return self.get_user(validated_token), validated_token
                except AuthenticationFailed:
                    return None
            else:
                return None
        elif validated_token is not None:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        
    def validate_token(self, token, key):
        try:
            decoded_token = jwt.decode(token, key, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return False

    def refresh_access_token(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return new_access_token
        except Exception as e:
            return None