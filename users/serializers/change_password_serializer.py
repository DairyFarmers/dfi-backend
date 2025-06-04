from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Your current password"
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        help_text="Your new password, must be at least 8 characters long"
    )

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password must be different from the old password.")
        return data
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("New password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("New password must contain at least one letter.")
        return value