from rest_framework import serializers

class SalesGraphSerializer(serializers.Serializer):
    order_date = serializers.DateField()
    total_sales = serializers.FloatField()