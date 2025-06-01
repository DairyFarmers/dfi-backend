from rest_framework import serializers
from users.models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", 
            "email", 
            "first_name", 
            "last_name", 
            "role",
            "is_active",
            "is_verified",
            "last_login",
        ]