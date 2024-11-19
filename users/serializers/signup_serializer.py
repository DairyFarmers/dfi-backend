from rest_framework import serializers
from users.models.user import User
import logging

logger = logging.getLogger(__name__)

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        max_length=128, 
        min_length=8
    )
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
    
    def validate(self, data):
        password = data.get('password')
        return data