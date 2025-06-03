from rest_framework import serializers
from users.models import UserSettings, UserContact, UserLocation

class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = [
            'id',
            'phone_primary',
            'phone_secondary',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserLocationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    location_type = serializers.ChoiceField(choices=[
        ('home', 'Home'),
        ('work', 'Work'),
        ('farm', 'Farm'),
        ('storage', 'Storage'),
        ('other', 'Other')
    ])
    is_primary = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserLocation
        fields = [
            'id',
            'location_type',
            'is_primary',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_location_type(self, value):
        valid_types = ['home', 'work', 'farm', 'storage', 'other']
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid location type. Must be one of: {', '.join(valid_types)}"
            )
        return value

    def to_representation(self, instance):
        """Handle both model instances and dictionaries"""
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)


class UserRoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.IntegerField()
    permissions = serializers.DictField()

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    contact = UserContactSerializer(read_only=True)
    locations = UserLocationSerializer(
        many=True, 
        read_only=True
    )
    role = UserRoleSerializer(read_only=True)
    created_at = serializers.DateTimeField()
    last_login = serializers.DateTimeField()

class UserSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    privacy_settings = serializers.JSONField()

    class Meta:
        model = UserSettings
        fields = [
            'id',
            'user',
            'privacy_settings',
            'created_at',
            'updated_at',
            'is_active'
        ]
        read_only_fields = [
            'id', 
            'user', 
            'created_at', 
            'updated_at'
        ]