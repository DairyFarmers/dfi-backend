from typing import Optional, List
from django.db.models.query import QuerySet
from suppliers.models import Supplier
from suppliers.repositories import SupplierRepository

class SupplierService:
    def __init__(self):
        self.repository = SupplierRepository()

    def get_all_suppliers(self) -> QuerySet[Supplier]:
        return self.repository.get_all()

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        return self.repository.get_by_id(supplier_id)

    def create_supplier(self, data: dict) -> Supplier:
        return self.repository.create(**data)

    def update_supplier(self, supplier_id: int, data: dict) -> Optional[Supplier]:
        supplier = self.get_supplier_by_id(supplier_id)
        if supplier:
            return self.repository.update(supplier, **data)
        return None

    def delete_supplier(self, supplier_id: int) -> bool:
        supplier = self.get_supplier_by_id(supplier_id)
        if supplier:
            return self.repository.delete(supplier)
        return False

    def search_suppliers(self, query: str) -> QuerySet[Supplier]:
        """Search suppliers by name, contact person, or email"""
        return self.repository.search(query)

    def get_suppliers_by_rating_range(self, min_rating: float, max_rating: float) -> QuerySet[Supplier]:
        return self.repository.get_by_rating_range(min_rating, max_rating)

    def get_active_suppliers(self) -> QuerySet[Supplier]:
        return self.repository.get_active_suppliers()

    def get_top_rated_suppliers(self, limit: int = 10) -> List[Supplier]:
        return list(self.repository.get_top_rated_suppliers(limit)) 