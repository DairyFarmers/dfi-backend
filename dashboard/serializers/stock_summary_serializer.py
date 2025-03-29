from rest_framework import serializers

class StockSummarySerializer(serializers.Serializer):
    total_stock = serializers.IntegerField()
    low_stock = serializers.IntegerField()

