from rest_framework import serializers

class ReportGenerateSerializer(serializers.Serializer):
    REPORT_TYPES = (
        ('sales', 'Sales Report'),
        ('inventory', 'Inventory Report'),
        ('orders', 'Orders Report'),
        ('user_activity', 'User Activity Report'),
    )
    
    FORMAT_TYPES = (
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    )

    report_type = serializers.ChoiceField(choices=REPORT_TYPES)
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()
    format = serializers.ChoiceField(choices=FORMAT_TYPES)
    filters = serializers.JSONField(required=False, default=dict)

    def validate(self, data):
        """
        Check that date_to is after date_from
        """
        if data['date_to'] < data['date_from']:
            raise serializers.ValidationError("End date must be after start date")
        return data