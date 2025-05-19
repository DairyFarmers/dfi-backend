from typing import Dict, List, Optional
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

    def get_items_by_order(self, order_id: int) -> List[OrderItem]:
        """Get all items for a specific order"""
        try:
            return self.repository.get_items_by_order(order_id)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving order items: {str(e)}')

    def get_items_by_inventory_item(self, inventory_item_id: int) -> List[OrderItem]:
        """Get all order items for a specific inventory item"""
        try:
            return self.repository.get_items_by_inventory_item(inventory_item_id)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving inventory items: {str(e)}')

    def get_total_quantity_sold(self, inventory_item_id: int) -> int:
        """Get total quantity sold for an inventory item"""
        try:
            return self.repository.get_total_quantity_sold(inventory_item_id)
        except RepositoryException as e:
            raise ServiceException(f'Error calculating total quantity: {str(e)}')

    def get_discounted_items(self) -> List[OrderItem]:
        """Get all items with discounts"""
        try:
            return self.repository.get_discounted_items()
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving discounted items: {str(e)}')

    def get_high_quantity_items(self, quantity_threshold: int = 10) -> List[OrderItem]:
        """Get items with quantity above threshold"""
        try:
            return self.repository.get_high_quantity_items(quantity_threshold)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving high quantity items: {str(e)}')

    def calculate_item_statistics(self, inventory_item_id: int) -> Dict:
        """Calculate statistics for a specific inventory item"""
        try:
            return self.repository.calculate_item_statistics(inventory_item_id)
        except RepositoryException as e:
            raise ServiceException(f'Error calculating item statistics: {str(e)}')

    def get_top_selling_items(self, limit: int = 10) -> List[Dict]:
        """Get top selling items by quantity"""
        try:
            return self.repository.get_top_selling_items(limit)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving top selling items: {str(e)}')

    def get_most_discounted_items(self, limit: int = 10) -> List[Dict]:
        """Get items with highest total discounts"""
        try:
            return self.repository.get_most_discounted_items(limit)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving most discounted items: {str(e)}') 