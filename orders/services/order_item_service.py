from typing import Dict, List, Optional, Any
from exceptions.exceptions import (
    RepositoryException,
    ServiceException
)
from orders.models import OrderItem

class OrderItemService:
    """
    Service layer for OrderItem-related business logic.
    """
    def __init__(self, repository):
        self.repository = repository

    def get_items_by_order(self, order_id: int, filters: Dict[str, Any] = None) -> List[OrderItem]:
        """Get all items for a specific order with optional filters"""
        try:
            base_filters = {'order_id': order_id}
            if filters:
                base_filters.update(filters)
            return self.repository.get_filtered(base_filters)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving order items: {str(e)}')

    def get_items_by_inventory_item(self, inventory_item_id: int, filters: Dict[str, Any] = None) -> List[OrderItem]:
        """Get all order items for a specific inventory item with optional filters"""
        try:
            base_filters = {'inventory_item_id': inventory_item_id}
            if filters:
                base_filters.update(filters)
            return self.repository.get_filtered(base_filters)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving inventory items: {str(e)}')

    def get_total_quantity_sold(self, inventory_item_id: int, filters: Dict[str, Any] = None) -> int:
        """Get total quantity sold for an inventory item with optional filters"""
        try:
            return self.repository.get_total_quantity_sold(inventory_item_id, filters)
        except RepositoryException as e:
            raise ServiceException(f'Error calculating total quantity: {str(e)}')

    def get_discounted_items(self, filters: Dict[str, Any] = None) -> List[OrderItem]:
        """Get all items with discounts and optional filters"""
        try:
            base_filters = {'discount__gt': 0}
            if filters:
                base_filters.update(filters)
            return self.repository.get_filtered(base_filters)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving discounted items: {str(e)}')

    def get_high_quantity_items(self, quantity_threshold: int = 10, filters: Dict[str, Any] = None) -> List[OrderItem]:
        """Get items with quantity above threshold and optional filters"""
        try:
            base_filters = {'quantity__gte': quantity_threshold}
            if filters:
                base_filters.update(filters)
            return self.repository.get_filtered(base_filters)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving high quantity items: {str(e)}')

    def calculate_item_statistics(self, inventory_item_id: int, filters: Dict[str, Any] = None) -> Dict:
        """Calculate statistics for a specific inventory item with optional filters"""
        try:
            return self.repository.calculate_item_statistics(inventory_item_id, filters)
        except RepositoryException as e:
            raise ServiceException(f'Error calculating item statistics: {str(e)}')

    def get_top_selling_items(self, limit: int = 10, filters: Dict[str, Any] = None) -> List[Dict]:
        """Get top selling items by quantity with optional filters"""
        try:
            return self.repository.get_top_selling_items(limit, filters)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving top selling items: {str(e)}')

    def get_most_discounted_items(self, limit: int = 10, filters: Dict[str, Any] = None) -> List[Dict]:
        """Get items with highest total discounts with optional filters"""
        try:
            return self.repository.get_most_discounted_items(limit, filters)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving most discounted items: {str(e)}')

    def search_items(self, search_term: str, filters: Dict[str, Any] = None) -> List[OrderItem]:
        """Search order items with optional filters"""
        try:
            search_filters = {
                'inventory_item__name__icontains': search_term,
                'order__order_number__icontains': search_term
            }
            if filters:
                search_filters.update(filters)
            return self.repository.get_filtered(search_filters)
        except RepositoryException as e:
            raise ServiceException(f'Error searching items: {str(e)}')