from rest_framework import serializers
from users.models.user import User
import re
import logging

logger = logging.getLogger(__name__)

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        max_length=128, 
        min_length=8
    )
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']
    
    def validate(self, data):
        password = data.get('password')
        role = data.get('role')
        
        if not self.is_strong_password(password):
            raise serializers.ValidationError(
                '''Password must contain at least 8 characters, 
                1 uppercase, 1 lowercase, 1 digit, 
                and 1 special character'''
            )
            
        return data
        
    def is_strong_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True