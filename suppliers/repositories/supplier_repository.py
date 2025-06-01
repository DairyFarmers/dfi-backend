from django.db.models import Q
from django.db.models.query import QuerySet
from django.db import DatabaseError
from suppliers.models import Supplier
from .base_repository import BaseRepository
from exceptions.exceptions import DatabaseException, RepositoryException
from utils import setup_logger

class SupplierRepository(BaseRepository[Supplier]):
    """Repository for supplier-specific operations"""
    def __init__(self):
        super().__init__(Supplier)
        self.logger = setup_logger(__name__)

    def search(self, query: str) -> QuerySet[Supplier]:
        """Search suppliers by name, contact person, or email"""
        try:
            self.logger.debug(f"Searching suppliers with query: {query}")
            suppliers = self.model_class.objects.filter(
                Q(name__icontains=query) |
                Q(contact_person__icontains=query) |
                Q(email__icontains=query)
            )
            self.logger.info(
                f"Found {suppliers.count()} suppliers matching query: {query}"
            )
            return suppliers
        except DatabaseError as e:
            self.logger.error(
                f"Database error while searching suppliers: {str(e)}"
            )
            raise RepositoryException(
                f"Database error during supplier search: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error while searching suppliers: {str(e)}"
            )
            raise RepositoryException(
                f"Error during supplier search: {str(e)}"
            )

    def get_by_rating_range(
            self, 
            min_rating: float, 
            max_rating: float
        ) -> QuerySet[Supplier]:
        """Get suppliers within a rating range"""
        try:
            self.logger.debug(
                f"Fetching suppliers with rating between {min_rating} and {max_rating}"
            )
            suppliers = self.model_class.objects.filter(
                rating__gte=min_rating,
                rating__lte=max_rating
            )
            self.logger.info(
                f"Found {suppliers.count()} suppliers in rating range"
            )
            return suppliers
        except DatabaseError as e:
            self.logger.error(
                f"Database error while fetching suppliers by rating: {str(e)}"
            )
            raise RepositoryException(
                f"Database error fetching suppliers by rating: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error while fetching suppliers by rating: {str(e)}"
            )
            raise RepositoryException(
                f"Error fetching suppliers by rating: {str(e)}"
            )

    def get_active_suppliers(self) -> QuerySet[Supplier]:
        """Get all active suppliers"""
        try:
            self.logger.debug("Fetching active suppliers")
            suppliers = self.model_class.objects.filter(is_active=True)
            self.logger.info(f"Found {suppliers.count()} active suppliers")
            return suppliers
        except DatabaseError as e:
            self.logger.error(
                f"Database error while fetching active suppliers: {str(e)}"
            )
            raise RepositoryException(
                f"Database error fetching active suppliers: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error while fetching active suppliers: {str(e)}"
            )
            raise RepositoryException(
                f"Error fetching active suppliers: {str(e)}"
            )

    def get_top_rated_suppliers(self, limit: int = 10) -> QuerySet[Supplier]:
        """Get top rated suppliers"""
        try:
            self.logger.debug(f"Fetching top {limit} rated suppliers")
            suppliers = self.model_class.objects.filter(
                is_active=True,
                rating__isnull=False
            ).order_by('-rating')[:limit]
            self.logger.info(f"Found {len(suppliers)} top rated suppliers")
            return suppliers
        except DatabaseError as e:
            self.logger.error(
                f"Database error while fetching top rated suppliers: {str(e)}"
            )
            raise RepositoryException(
                f"Database error fetching top rated suppliers: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error while fetching top rated suppliers: {str(e)}"
            )
            raise RepositoryException(
                f"Error fetching top rated suppliers: {str(e)}"
            )