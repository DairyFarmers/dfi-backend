from typing import Optional, List
from django.db.models.query import QuerySet
from suppliers.models import Supplier
from suppliers.repositories import SupplierRepository
from exceptions.exceptions import RepositoryException, ServiceException
from utils import setup_logger

class SupplierService:
    def __init__(self):
        self.repository = SupplierRepository()
        self.logger = setup_logger(__name__)

    def get_all_suppliers(self) -> QuerySet[Supplier]:
        try:
            self.logger.debug("Fetching all suppliers")
            return self.repository.get_all()
        except RepositoryException as e:
            self.logger.error(f"Error fetching all suppliers: {str(e)}")
            raise ServiceException(f"Failed to fetch suppliers: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error fetching suppliers: {str(e)}")
            raise ServiceException(
                "An unexpected error occurred while fetching suppliers"
            )

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        try:
            self.logger.debug(f"Fetching supplier with ID: {supplier_id}")
            return self.repository.get_by_id(supplier_id)
        except RepositoryException as e:
            self.logger.error(f"Error fetching supplier {supplier_id}: {str(e)}")
            raise ServiceException(f"Failed to fetch supplier: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching supplier {supplier_id}: {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while fetching supplier"
            )

    def create_supplier(self, data: dict) -> Supplier:
        try:
            self.logger.debug(f"Creating supplier with data: {data}")
            return self.repository.create(**data)
        except RepositoryException as e:
            self.logger.error(f"Error creating supplier: {str(e)}")
            raise ServiceException(f"Failed to create supplier: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"Unexpected error creating supplier: {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while creating supplier"
            )

    def update_supplier(self, supplier_id: int, data: dict) -> Optional[Supplier]:
        try:
            self.logger.debug(
                f"Updating supplier with ID {supplier_id} with data: {data}"
            )
            supplier = self.get_supplier_by_id(supplier_id)
            if supplier:
                return self.repository.update(supplier, **data)
            return None
        except RepositoryException as e:
            self.logger.error(f"Error updating supplier {supplier_id}: {str(e)}")
            raise ServiceException(f"Failed to update supplier: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"Unexpected error updating supplier {supplier_id}: {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while updating supplier"
            )

    def delete_supplier(self, supplier_id: int) -> bool:
        try:
            self.logger.debug(f"Deleting supplier with ID: {supplier_id}")
            supplier = self.get_supplier_by_id(supplier_id)
            if supplier:
                return self.repository.delete(supplier)
            return False
        except RepositoryException as e:
            self.logger.error(f"Error deleting supplier {supplier_id}: {str(e)}")
            raise ServiceException(f"Failed to delete supplier: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"Unexpected error deleting supplier {supplier_id}: {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while deleting supplier"
            )

    def search_suppliers(self, query: str) -> QuerySet[Supplier]:
        try:
            self.logger.debug(f"Searching suppliers with query: {query}")
            return self.repository.search(query)
        except RepositoryException as e:
            self.logger.error(f"Error searching suppliers: {str(e)}")
            raise ServiceException(f"Failed to search suppliers: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error searching suppliers: {str(e)}")
            raise ServiceException(
                "An unexpected error occurred while searching suppliers"
            )

    def get_suppliers_by_rating_range(
            self, 
            min_rating: float, 
            max_rating: float
        ) -> QuerySet[Supplier]:
        try:
            self.logger.debug(
                f"Fetching suppliers with rating between {min_rating} and {max_rating}"
            )
            return self.repository.get_by_rating_range(min_rating, max_rating)
        except RepositoryException as e:
            self.logger.error(f"Error fetching suppliers by rating: {str(e)}")
            raise ServiceException(
                f"Failed to fetch suppliers by rating: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching suppliers by rating: {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while fetching suppliers by rating"
            )

    def get_active_suppliers(self) -> QuerySet[Supplier]:
        try:
            self.logger.debug("Fetching active suppliers")
            return self.repository.get_active_suppliers()
        except RepositoryException as e:
            self.logger.error(f"Error fetching active suppliers: {str(e)}")
            raise ServiceException(
                f"Failed to fetch active suppliers: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching active suppliers: {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while fetching active suppliers"
            )

    def get_top_rated_suppliers(self, limit: int = 10) -> List[Supplier]:
        try:
            self.logger.debug(f"Fetching top {limit} rated suppliers")
            return list(self.repository.get_top_rated_suppliers(limit))
        except RepositoryException as e:
            self.logger.error(f"Error fetching top rated suppliers: {str(e)}")
            raise ServiceException(
                f"Failed to fetch top rated suppliers: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching top rated suppliers:\ {str(e)}"
            )
            raise ServiceException(
                "An unexpected error occurred while fetching top rated suppliers"
            )