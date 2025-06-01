from rest_framework import serializers
from users.models import B2BUser

class B2BUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = B2BUser
        fields = [
            'username', 'email', 'password', 'company_name',
            'business_type', 'tax_id'
        ]