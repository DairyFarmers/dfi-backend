from rest_framework import serializers

class InventoryItemBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer with common validation logic for inventory items.
    """
    def validate(self, data):
        if 'optimal_temperature_min' in data and 'optimal_temperature_max' in data:
            if data['optimal_temperature_min'] >= data['optimal_temperature_max']:
                raise serializers.ValidationError(
                    "Minimum temperature must be less than maximum temperature"
                )

        if 'manufacturing_date' in data and 'expiry_date' in data:
            if data['manufacturing_date'] >= data['expiry_date']:
                raise serializers.ValidationError(
                    "Manufacturing date must be before expiry date"
                )

        return data 