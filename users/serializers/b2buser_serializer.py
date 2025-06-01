from rest_framework import serializers
from users.models import B2BUser

class B2BUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BUser
        fields = [
            'id', 'username', 'email', 'company_name', 
            'business_type', 'tax_id', 'credit_limit',
            'payment_terms', 'is_approved', 'approval_date'
        ]
        read_only_fields = ['id', 'approval_date', 'is_approved']

