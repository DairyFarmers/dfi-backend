from rest_framework import serializers
from users.models import Passcode
import logging

logger = logging.getLogger(__name__)

class EmailVerificationSerializer(serializers.Serializer):
    passcode = serializers.CharField(max_length=8)
    is_verified = serializers.BooleanField(required=False)
    
    class Meta:
        model = Passcode
        fields = ['passcode', 'is_verified']
                  
    def validate(self, data):
        passcode = data.get('passcode') 
        if not passcode:
            raise serializers.ValidationError('Passcode is required!')
        return data