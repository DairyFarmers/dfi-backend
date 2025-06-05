from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError
from exceptions import InvalidDataException

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    uid = serializers.CharField(min_length=5, write_only=True)
    token = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, data):
        password = data.get('password')
        token = data.get('token')
        uidb64 = data.get('uid')
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
        except (TypeError, ValueError, OverflowError):
            raise InvalidDataException('Invalid user ID')
        except ValidationError as e:
            raise ValidationError('Invalid user ID')
        
        return {
            'user_id': user_id,
            'password': password,
            'token': token
        }