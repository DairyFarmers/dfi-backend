# chat/serializers.py
from rest_framework import serializers
from chats.models.chat import Message
from users.models.user import User

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 
            'last_name',
            'email',
            'role_name'
        ]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 
            'sender', 
            'receiver', 
            'text', 
            'timestamp', 
            'is_read',
        ]
        read_only_fields = [
            'sender', 
            'timestamp', 
            'is_read'
        ]

class ChatPreviewSerializer(serializers.Serializer):
    user = UserSerializer()
    last_message = serializers.CharField()
    unread_count = serializers.IntegerField()
    timestamp = serializers.DateTimeField()