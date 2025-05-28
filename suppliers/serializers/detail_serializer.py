from suppliers.models import Supplier
from .base_serializer import SupplierBaseSerializer

class SupplierDetailSerializer(SupplierBaseSerializer):
    """
    Serializer for detailed supplier information.
    """
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'is_active'] 