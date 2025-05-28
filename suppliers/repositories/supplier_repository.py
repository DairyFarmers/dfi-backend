from django.db.models import Q
from django.db.models.query import QuerySet
from suppliers.models import Supplier
from .base_repository import BaseRepository

class SupplierRepository(BaseRepository[Supplier]):
    """Repository for supplier-specific operations"""
    def __init__(self):
        super().__init__(Supplier)

    def search(self, query: str) -> QuerySet[Supplier]:
        """Search suppliers by name, contact person, or email"""
        return self.model_class.objects.filter(
            Q(name__icontains=query) |
            Q(contact_person__icontains=query) |
            Q(email__icontains=query)
        )

    def get_by_rating_range(self, min_rating: float, max_rating: float) -> QuerySet[Supplier]:
        """Get suppliers within a rating range"""
        return self.model_class.objects.filter(
            rating__gte=min_rating,
            rating__lte=max_rating
        )

    def get_active_suppliers(self) -> QuerySet[Supplier]:
        """Get all active suppliers"""
        return self.model_class.objects.filter(is_active=True)

    def get_top_rated_suppliers(self, limit: int = 10) -> QuerySet[Supplier]:
        """Get top rated suppliers"""
        return self.model_class.objects.filter(
            is_active=True,
            rating__isnull=False
        ).order_by('-rating')[:limit] 