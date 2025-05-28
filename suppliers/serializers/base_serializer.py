from rest_framework import serializers

class SupplierBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer with common validation logic for suppliers.
    """
    def validate_rating(self, value):
        """Validate rating is between 0 and 5"""
        if value and (value < 0 or value > 5):
            raise serializers.ValidationError("Rating must be between 0 and 5")
        return value 