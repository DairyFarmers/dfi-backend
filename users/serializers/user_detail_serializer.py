from rest_framework import serializers
from users.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'role_name',
            'is_active',
            'last_login',
            'date_joined'
        ]
        read_only_fields = ['id', 'email', 'last_login', 'date_joined']