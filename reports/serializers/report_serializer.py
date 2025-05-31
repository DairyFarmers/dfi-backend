from rest_framework import serializers
from reports.models import Report
from users.serializers.user_serializer import UserSerializer

class ReportSerializer(serializers.ModelSerializer):
    generated_by = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'report_type', 'format', 'status', 
            'generated_by', 'generated_at', 'date_from', 
            'date_to', 'filters', 'error_message', 'file_url'
        ]
        read_only_fields = ['id', 'status', 'generated_by', 'generated_at', 'file_url']

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None