from rest_framework import serializers
from notifications.models import Notification
from users.serializers.user_serializer import UserSerializer
from django.utils import timezone

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'title',
            'message',
            'user',
            'read',
            'created_at',
            'sent_email',
            'related_object_id',
            'related_object_type'
        ]
        read_only_fields = [
            'id', 
            'type', 
            'title', 
            'message', 
            'user', 
            'created_at', 
            'sent_email',
            'related_object_id',
            'related_object_type'
        ]

    def to_representation(self, instance):
        """Customize the notification representation"""
        data = super().to_representation(instance)
        
        # Add relative time for frontend display
        created_at = instance.created_at
        now = timezone.now()
        time_diff = now - created_at

        if time_diff.days > 0:
            relative_time = f"{time_diff.days} days ago"
        elif time_diff.seconds >= 3600:
            hours = time_diff.seconds // 3600
            relative_time = f"{hours} hours ago"
        elif time_diff.seconds >= 60:
            minutes = time_diff.seconds // 60
            relative_time = f"{minutes} minutes ago"
        else:
            relative_time = "just now"

        data['relative_time'] = relative_time
        
        # Add notification priority based on type
        priority_map = {
            'expiry': 'high',
            'low_stock': 'medium',
            'price_change': 'low',
            'order_status': 'medium',
            'payment_due': 'high'
        }
        data['priority'] = priority_map.get(instance.type, 'low')

        return data