from rest_framework import serializers

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=100, required=False, read_only=True)
    
    class Meta:
        fields = ['email', 'first_name']

    def validate(self, data):
        email = data.get('email')
        return data