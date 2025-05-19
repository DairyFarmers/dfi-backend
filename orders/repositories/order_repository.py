from django.db.models import Q, QuerySet, Count, Sum, F
from django.utils import timezone
from typing import Dict, List, Optional
from datetime import datetime, date

from repositories.base_repository import BaseRepository
from django.db import models, DatabaseError
from exceptions.exceptions import DatabaseException

from orders.models import Order

class OrderRepository(BaseRepository):
    """
    Repository for Order model operations.
    """
    model_class = Order

    def __init__(self, model: models.Model):
        super().__init__(model)

    def get_queryset(self) -> QuerySet:
        """Get base queryset with common annotations"""
        return super().get_queryset().prefetch_related('items')

    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number"""
        return self.get_queryset().filter(order_number=order_number).first()

    def get_customer_orders(self, customer_email: str) -> QuerySet:
        """Get all orders for a customer"""
        return self.get_queryset().filter(customer_email=customer_email)

    def get_orders_by_status(self, status: str) -> QuerySet:
        """Get orders by status"""
        return self.get_queryset().filter(status=status)

    def get_orders_by_date_range(self, start_date: date, end_date: date) -> QuerySet:
        """Get orders within a date range"""
        return self.get_queryset().filter(
            order_date__date__gte=start_date,
            order_date__date__lte=end_date
        )

    def get_overdue_orders(self) -> QuerySet:
        """Get all overdue orders"""
        today = timezone.now().date()
        return self.get_queryset().filter(
            expected_delivery_date__lt=today,
            status__in=['pending', 'confirmed', 'processing', 'shipped']
        )

    def get_orders_by_priority(self, priority: str) -> QuerySet:
        """Get orders by priority level"""
        return self.get_queryset().filter(priority=priority)

    def get_orders_by_payment_status(self, payment_status: str) -> QuerySet:
        """Get orders by payment status"""
        return self.get_queryset().filter(payment_status=payment_status)

    def search_orders(self, search_term: str) -> QuerySet:
        """Search orders by various fields"""
        return self.get_queryset().filter(
            Q(order_number__icontains=search_term) |
            Q(customer_name__icontains=search_term) |
            Q(customer_email__icontains=search_term) |
            Q(tracking_number__icontains=search_term)
        )

    def get_order_statistics(self, start_date: date, end_date: date) -> Dict:
        """Get order statistics for a date range"""
        orders = self.get_orders_by_date_range(start_date, end_date)
        return {
            'total_orders': orders.count(),
            'total_amount': orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'status_counts': orders.values('status').annotate(count=Count('id')),
            'payment_status_counts': orders.values('payment_status').annotate(count=Count('id'))
        }

    def get_customer_statistics(self, customer_email: str) -> Dict:
        """Get statistics for a specific customer"""
        orders = self.get_customer_orders(customer_email)
        return {
            'total_orders': orders.count(),
            'total_spent': orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'average_order_value': orders.aggregate(avg=Sum('total_amount') / Count('id'))['avg'] or 0,
            'order_status_counts': orders.values('status').annotate(count=Count('id'))
        }

    def get_orders_with_items_count(self) -> QuerySet:
        """Get orders with their item counts"""
        return self.get_queryset().annotate(items_count=Count('items'))

    def get_high_value_orders(self, threshold: float = 1000.0) -> QuerySet:
        """Get orders above a certain value threshold"""
        return self.get_queryset().filter(total_amount__gte=threshold)

    def get_recent_orders(self, days: int = 30) -> QuerySet:
        """Get orders from the last N days"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.get_queryset().filter(order_date__gte=cutoff_date)

    def get_by_id(self, item_id):
        try:
            return self.model.objects.get(id=item_id)
        except self.model.DoesNotExist:
            raise DatabaseException('Item not found')
        except DatabaseError as e:
            raise DatabaseException('Error while retrieving item')
        
    def get_all(self):
        try:
            return self.model.objects.all()
        except DatabaseError as e:
            raise DatabaseException('Error while retrieving items')
        
    def get_only(self, item_id, *fields):
        try:
            return self.model.objects.only(*fields).get(id=item_id)
        except self.model.DoesNotExist:
            raise DatabaseException('Item not found')
        except DatabaseError as e:
            raise DatabaseException('Error while retrieving item')
    
    def create(self, data):
        try:
            return self.model.objects.create(**data)
        except DatabaseError as e:
            raise DatabaseException('Error while adding item')

    def update(self, id, **kwargs):
        try:
            instance = self.get_by_id(id)
            if not instance: return None
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except DatabaseError as e:
            raise DatabaseException('Error while updating item')

    def delete(self, id):
        try:
            instance = self.get_by_id(id)
            if not instance: return False
            instance.delete()
            return True
        except DatabaseError as e:
            raise DatabaseException('Error while deleting item')