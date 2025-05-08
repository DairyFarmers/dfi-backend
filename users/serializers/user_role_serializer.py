from rest_framework import serializers
from users.models.user_role import UserRole

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'description', 'permissions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        # Convert to lowercase and replace spaces with underscores
        value = value.lower().replace(' ', '_')
        
        # Check if role with this name already exists
        if UserRole.objects.filter(name=value).exists():
            if self.instance and self.instance.name == value:
                return value
            raise serializers.ValidationError("A role with this name already exists.")
        return value

    def validate_permissions(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Permissions must be a dictionary")
        return value 