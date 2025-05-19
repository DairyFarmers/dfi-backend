from django.db.models import QuerySet, Sum, F
from typing import List, Optional

from orders.models import OrderItem
from .base_repository import BaseRepository

class OrderItemRepository(BaseRepository):
    """
    Repository for OrderItem model operations.
    """
    model_class = OrderItem

    def get_queryset(self) -> QuerySet:
        """Get base queryset with related fields"""
        return super().get_queryset().select_related('order', 'inventory_item')

    def get_items_by_order(self, order_id: int) -> QuerySet:
        """Get all items for a specific order"""
        return self.get_queryset().filter(order_id=order_id)

    def get_items_by_inventory_item(self, inventory_item_id: int) -> QuerySet:
        """Get all order items for a specific inventory item"""
        return self.get_queryset().filter(inventory_item_id=inventory_item_id)

    def get_total_quantity_sold(self, inventory_item_id: int) -> int:
        """Get total quantity sold for an inventory item"""
        result = self.get_items_by_inventory_item(inventory_item_id)\
            .aggregate(total_quantity=Sum('quantity'))
        return result['total_quantity'] or 0

    def get_items_above_price(self, price_threshold: float) -> QuerySet:
        """Get items above a certain unit price"""
        return self.get_queryset().filter(unit_price__gte=price_threshold)

    def get_discounted_items(self) -> QuerySet:
        """Get all items with discounts"""
        return self.get_queryset().filter(discount__gt=0)

    def get_high_quantity_items(self, quantity_threshold: int = 10) -> QuerySet:
        """Get items with quantity above threshold"""
        return self.get_queryset().filter(quantity__gte=quantity_threshold)

    def get_items_by_order_status(self, status: str) -> QuerySet:
        """Get items from orders with specific status"""
        return self.get_queryset().filter(order__status=status)

    def calculate_item_statistics(self, inventory_item_id: int) -> dict:
        """Calculate statistics for a specific inventory item"""
        items = self.get_items_by_inventory_item(inventory_item_id)
        stats = items.aggregate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('unit_price') - F('discount')),
            total_discount=Sum('discount')
        )
        return {
            'total_quantity': stats['total_quantity'] or 0,
            'total_revenue': stats['total_revenue'] or 0,
            'total_discount': stats['total_discount'] or 0,
            'order_count': items.values('order').distinct().count()
        }

    def get_top_selling_items(self, limit: int = 10) -> QuerySet:
        """Get top selling items by quantity"""
        return self.get_queryset()\
            .values('inventory_item__name')\
            .annotate(total_quantity=Sum('quantity'))\
            .order_by('-total_quantity')[:limit]

    def get_most_discounted_items(self, limit: int = 10) -> QuerySet:
        """Get items with highest total discounts"""
        return self.get_queryset()\
            .values('inventory_item__name')\
            .annotate(total_discount=Sum('discount'))\
            .filter(total_discount__gt=0)\
            .order_by('-total_discount')[:limit] 