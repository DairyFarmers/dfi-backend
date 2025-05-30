from typing import Dict, List, Optional
from datetime import date
from django.utils import timezone

from exceptions.exceptions import (
    RepositoryException,
    ServiceException
)
from orders.models import Order, OrderItem

class OrderService:
    """
    Service layer for Order-related business logic.
    """
    def __init__(self, order_repository, order_item_repository):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository

    def get_all_orders(self):
        """Get all active orders"""
        try:
            return self.order_repository.get_all()
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving orders: {str(e)}')

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Get order by ID"""
        try:
            return self.order_repository.get_by_id(order_id)
        except RepositoryException as e:
            raise ServiceException(f'Order not found: {str(e)}')

    def create_order(self, order_data: Dict, items_data: List[Dict]) -> Order:
        """Create a new order with items"""
        try:
            # Create order
            order = self.order_repository.create(order_data)
            
            # Create order items
            for item_data in items_data:
                item_data['order'] = order
                self.order_item_repository.create(item_data)
            
            # Calculate total
            order.calculate_total()
            return order
        except RepositoryException as e:
            raise ServiceException(f'Error creating order: {str(e)}')

    def update_order(self, order_id: int, order_data: Dict, items_data: Optional[List[Dict]] = None) -> Order:
        """Update an order and optionally its items"""
        try:
            order = self.get_order_by_id(order_id)
            if not order:
                raise ServiceException('Order not found')

            if not order.can_modify():
                raise ServiceException('Order cannot be modified in its current state')

            # Update order
            order = self.order_repository.update(order, order_data)

            # Update items if provided
            if items_data is not None:
                # Delete existing items
                order.items.all().delete()
                
                # Create new items
                for item_data in items_data:
                    item_data['order'] = order
                    self.order_item_repository.create(item_data)

            # Recalculate total
            order.calculate_total()
            return order
        except RepositoryException as e:
            raise ServiceException(f'Error updating order: {str(e)}')

    def delete_order(self, order_id: int) -> bool:
        """Soft delete an order"""
        try:
            order = self.get_order_by_id(order_id)
            if not order:
                raise ServiceException('Order not found')
            return self.order_repository.delete(order)
        except RepositoryException as e:
            raise ServiceException(f'Error deleting order: {str(e)}')

    def cancel_order(self, order_id: int) -> Order:
        """Cancel an order"""
        try:
            order = self.get_order_by_id(order_id)
            if not order:
                raise ServiceException('Order not found')
            
            if not order.can_cancel():
                raise ServiceException('Order cannot be cancelled in its current state')
            
            order.status = 'cancelled'
            order.save()
            return order
        except RepositoryException as e:
            raise ServiceException(f'Error cancelling order: {str(e)}')

    def mark_delivered(self, order_id: int) -> Order:
        """Mark an order as delivered"""
        try:
            order = self.get_order_by_id(order_id)
            if not order:
                raise ServiceException('Order not found')
            
            if order.status != 'shipped':
                raise ServiceException('Only shipped orders can be marked as delivered')
            
            order.status = 'delivered'
            order.actual_delivery_date = timezone.now().date()
            order.save()
            return order
        except RepositoryException as e:
            raise ServiceException(f'Error marking order as delivered: {str(e)}')

    def get_customer_orders(self, customer_email: str):
        """Get all orders for a customer"""
        try:
            return self.order_repository.get_customer_orders(customer_email)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving customer orders: {str(e)}')

    def get_order_statistics(self, start_date: date, end_date: date) -> Dict:
        """Get order statistics for a date range"""
        try:
            return self.order_repository.get_order_statistics(start_date, end_date)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving order statistics: {str(e)}')

    def get_overdue_orders(self):
        """Get all overdue orders"""
        try:
            return self.order_repository.get_overdue_orders()
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving overdue orders: {str(e)}')

    def get_high_value_orders(self, threshold: float = 1000.0):
        """Get high-value orders"""
        try:
            return self.order_repository.get_high_value_orders(threshold)
        except RepositoryException as e:
            raise ServiceException(f'Error retrieving high-value orders: {str(e)}')