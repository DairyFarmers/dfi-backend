from rest_framework import serializers
from users.models import User
import logging

logger = logging.getLogger(__name__)

class LoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=255, write_only=True)
    full_name = serializers.CharField(max_length=60, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'full_name', 
            'password', 
            'access_token', 
            'refresh_token', 
            'is_verified'
        ]
                  
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')   
        return data
        
        