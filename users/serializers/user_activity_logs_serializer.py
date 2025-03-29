from rest_framework import serializers
from users.models.user_activity_log import UserActivityLog

class UserActivityLogsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserActivityLog
        fields = ["id", "user", "action", "timestamp", "ip_address"]