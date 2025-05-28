from suppliers.models import Supplier
from .base_serializer import SupplierBaseSerializer

class SupplierCreateUpdateSerializer(SupplierBaseSerializer):
    """
    Serializer for creating and updating suppliers.
    """
    class Meta:
        model = Supplier
        fields = [
            'name', 'contact_person', 'email', 'phone',
            'address', 'rating', 'notes'
        ] 