from rest_framework import serializers
from reports.models.report import Report

class ReportSerializer(serializers.ModelSerializer):
    generated_by = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = ["id", "title", "report_type", "generated_by", "generated_at", "data", "file_url"]