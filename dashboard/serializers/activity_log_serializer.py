from rest_framework import serializers
from users.models.user_activity_log import UserActivityLog
from users.models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

class UserActivityLogSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'user_details', 'action', 'timestamp', 'ip_address']
        read_only_fields = fields 