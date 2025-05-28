from suppliers.models import Supplier
from .base_serializer import SupplierBaseSerializer

class SupplierListSerializer(SupplierBaseSerializer):
    """
    Serializer for listing suppliers with basic fields.
    """
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'email',
            'rating', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_active'] 