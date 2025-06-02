from rest_framework import serializers
from notifications.models import Notification
from users.serializers.user_serializer import UserSerializer
from django.utils import timezone

class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # Explicitly define id field
    notification_type = serializers.CharField(read_only=True)
    notification_title = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    priority = serializers.CharField(read_only=True)
    read = serializers.BooleanField(default=False)
    
    # Define formatted datetime fields
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    read_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, allow_null=True)
    
    # Define relationship fields
    user = UserSerializer(read_only=True)
    related_object_id = serializers.UUIDField(allow_null=True, read_only=True)
    related_object_type = serializers.CharField(allow_null=True, read_only=True)
    
    # Define computed fields
    redirect_url = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    is_urgent = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'priority',
            'notification_title',
            'message',
            'user',
            'read',
            'read_at',
            'created_at',
            'updated_at',
            'sent_email',
            'related_object_id',
            'related_object_type',
            'redirect_url',
            'relative_time',
            'is_recent',
            'is_urgent'
        ]

    def get_redirect_url(self, obj):
        """Get the redirect URL for the notification"""
        if not obj or not isinstance(obj, Notification):
            return None
            
        if not obj.related_object_id or not obj.related_object_type:
            return None

        return obj.get_redirect_url()


    def get_relative_time(self, obj):
        """Get relative time string"""
        if not obj or not isinstance(obj, Notification):
            return ""
            
        now = timezone.now()
        time_diff = now - obj.created_at

        if time_diff.days > 7:
            return obj.created_at.strftime("%Y-%m-%d %H:%M")
        elif time_diff.days > 0:
            return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        elif time_diff.seconds >= 3600:
            hours = time_diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif time_diff.seconds >= 60:
            minutes = time_diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        return "just now"

    def get_is_recent(self, obj):
        """Check if notification is less than 24 hours old"""
        if not obj or not isinstance(obj, Notification):
            return False
        return (timezone.now() - obj.created_at).days < 1

    def get_is_urgent(self, obj):
        """Check if notification is urgent"""
        if not obj or not isinstance(obj, Notification):
            return False
            
        is_high_priority = obj.priority in ['high', 'urgent']
        if obj.notification_type == 'expiry':
            try:
                days_until_expiry = int(obj.message.split()[3])
                return days_until_expiry <= 7 or is_high_priority
            except (IndexError, ValueError):
                return is_high_priority
        return is_high_priority