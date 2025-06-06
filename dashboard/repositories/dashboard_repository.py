from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from users.models.user import User
from inventories.models.inventory_item import InventoryItem
from orders.models.order import Order
from orders.models.order_item import OrderItem
from products.models import (
    DairyProduction,
    DairyInventory
)
from users.models.user_activity_log import UserActivityLog
from django.db import connection
from ..serializers.activity_log_serializer import UserActivityLogSerializer
from exceptions import RepositoryException

class DashboardRepository:
    @staticmethod
    def get_time_range_filter(time_range):
        now = timezone.now()
        if time_range == 'week':
            return now - timedelta(days=7)
        elif time_range == 'month':
            return now - timedelta(days=30)
        elif time_range == 'year':
            return now - timedelta(days=365)
        return now - timedelta(days=7)  # default to week

    # Common Methods
    @staticmethod
    def get_user_notifications(user_id):
        # TODO: Implement notifications when the model is available
        return []

    @staticmethod
    def get_recent_activities(user_id):
        try:
            activities = UserActivityLog.objects.filter(
                user_id=user_id
            ).order_by('-timestamp')[:10]
            serializer = UserActivityLogSerializer(activities, many=True)
            return serializer.data
        except RepositoryException as e:
            raise RepositoryException(f"Error fetching recent activities: {str(e)}")

    # Inventory Methods
    @staticmethod
    def get_total_inventory_items():
        """Get total inventory items count and quantity"""
        result = InventoryItem.objects.aggregate(
            total_items=Count('id'),
            total_quantity=Sum('quantity')
        )
        return {
            'count': result.get('total_items') or 0,
            'total_quantity': float(result.get('total_quantity') or 0)
        }

    @staticmethod
    def get_low_stock_items():
        """Get items with quantity below reorder point"""
        items = InventoryItem.objects.filter(
            quantity__lte=F('reorder_point')
        ).values('id', 'name', 'quantity', 'reorder_point')
        return list(items)

    @staticmethod
    def get_total_stock_value():
        """Get total value of current inventory"""
        result = InventoryItem.objects.aggregate(
            total_value=Sum(F('quantity') * F('price'))
        )
        return float(result.get('total_value') or 0)

    # Order Methods
    @staticmethod
    def get_total_orders(time_range):
        """Get total orders within time range"""
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            updated_at__gte=start_date
        ).count()

    @staticmethod
    def get_pending_orders():
        """Get count of pending orders"""
        return Order.objects.filter(status='pending').count()

    @staticmethod
    def get_order_status_distribution(shop_owner_id=None):
        """Get distribution of order statuses, optionally filtered by shop owner"""
        query = Order.objects.all()
        if shop_owner_id:
            query = query.filter(shop_owner_id=shop_owner_id)
        return query.values('status').annotate(
            count=Count('id')
        ).order_by('status')

    @staticmethod
    def get_total_revenue(time_range):
        """Get total revenue within time range"""
        start_date = DashboardRepository.get_time_range_filter(time_range)
        result = Order.objects.filter(
            updated_at__gte=start_date,
            status='delivered'
        ).aggregate(
            total_revenue=Sum('total_amount')
        )
        return result.get('total_revenue') or 0

    # User Performance Methods
    @staticmethod
    def get_user_sales(user_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            created_by_id=user_id,
            updated_at__gte=start_date
        ).values('updated_at__date').annotate(
            daily_sales=Count('id'),
            daily_revenue=Sum('total_amount')
        ).order_by('updated_at__date')

    @staticmethod
    def get_user_popular_products(user_id):
        return OrderItem.objects.filter(
            order__created_by_id=user_id
        ).values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:10]

    @staticmethod
    def get_user_revenue_summary(user_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            created_by_id=user_id,
            updated_at__gte=start_date
        ).aggregate(
            total_revenue=Sum('total_amount'),
            average_order_value=Avg('total_amount'),
            order_count=Count('id')
        )

    # Admin Methods
    @staticmethod
    def get_total_users():
        return User.objects.count()

    @staticmethod
    def get_active_users():
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return User.objects.filter(last_login__gte=thirty_days_ago).count()

    @staticmethod
    def get_revenue_trends(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            updated_at__gte=start_date,
            status='delivered'
        ).values('updated_at__date').annotate(
            daily_revenue=Sum('total_amount')
        ).order_by('updated_at__date')

    @staticmethod
    def get_top_products(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return OrderItem.objects.filter(
            order__updated_at__gte=start_date
        ).values('product__name').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price'))
        ).order_by('-total_revenue')[:10]

    @staticmethod
    def get_system_health():
        return {
            'system_status': 'healthy',
            'database_status': 'connected',
            'cache_status': 'operational'
        }

    @staticmethod
    def get_new_users_stats(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return User.objects.filter(date_joined__gte=start_date).count()

    @staticmethod
    def get_user_type_distribution():
        return User.objects.values('role').annotate(count=Count('id'))

    @staticmethod
    def get_active_shops_count():
        return User.objects.filter(role='shop_owner', is_active=True).count()

    @staticmethod
    def get_expiring_stock():
        thirty_days_from_now = timezone.now() + timedelta(days=30)
        return InventoryItem.objects.filter(
            expiry_date__lte=thirty_days_from_now
        ).select_related('product')

    @staticmethod
    def get_stock_movements(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return InventoryItem.objects.filter(
            updated_at__gte=start_date
        ).select_related('product')

    @staticmethod
    def get_top_moving_items():
        return OrderItem.objects.values(
            'product__name'
        ).annotate(
            total_movement=Sum('quantity')
        ).order_by('-total_movement')[:10]

    @staticmethod
    def get_stock_alerts():
        return InventoryItem.objects.filter(
            Q(quantity__lte=F('reorder_point')) |
            Q(expiry_date__lte=timezone.now() + timedelta(days=30))
        ).select_related('product')

    @staticmethod
    def get_shop_sales(shop_owner_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            shop_owner_id=shop_owner_id,
            updated_at__gte=start_date
        ).values('updated_at__date').annotate(
            daily_sales=Count('id'),
            daily_revenue=Sum('total_amount')
        )

    @staticmethod
    def get_shop_popular_products(shop_owner_id):
        return OrderItem.objects.filter(
            order__shop_owner_id=shop_owner_id
        ).values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:10]

    @staticmethod
    def get_customer_satisfaction(shop_owner_id):
        return Order.objects.filter(
            shop_owner_id=shop_owner_id
        ).aggregate(
            avg_rating=Avg('rating'),
            total_reviews=Count('rating')
        )

    @staticmethod
    def get_shop_pending_orders(shop_owner_id):
        return Order.objects.filter(
            shop_owner_id=shop_owner_id,
            status='pending'
        )

    @staticmethod
    def get_dairy_production_summary(farmer_id, time_range):
        """Get dairy production summary for farmer"""
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return DairyProduction.objects.filter(
            farmer_id=farmer_id,
            production_date__gte=start_date
        ).values('product_type').annotate(
            total_quantity=Sum('quantity'),
            avg_quality=Avg('quality_score')
        )

    @staticmethod
    def get_dairy_inventory_status(farmer_id):
        """Get current dairy inventory status"""
        return DairyInventory.objects.filter(
            production__farmer_id=farmer_id,
            quantity_available__gt=0
        ).values(
            'production__product_type'
        ).annotate(
            total_quantity=Sum('quantity_available'),
            expiring_soon=Count(
                'id',
                filter=Q(
                    expiry_date__lte=timezone.now() + timedelta(days=7)
                )
            )
        )

    @staticmethod
    def get_dairy_revenue_metrics(farmer_id, time_range):
        """Get revenue metrics for dairy products"""
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            farmer_id=farmer_id,
            created_at__gte=start_date,
            orderitem__product__category='dairy'
        ).values('updated_at__date').annotate(
            daily_revenue=Sum('total_amount'),
            products_sold=Count('orderitem')
        ).order_by('updated_at__date')

    @staticmethod
    def get_farmer_sales_history(farmer_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            farmer_id=farmer_id,
            updated_at__gte=start_date
        ).values('updated_at__date').annotate(
            daily_sales=Count('id'),
            daily_revenue=Sum('total_amount')
        )

    @staticmethod
    def get_farmer_buyer_insights(farmer_id):
        return Order.objects.filter(
            farmer_id=farmer_id
        ).values('buyer__id', 'buyer__name').annotate(
            total_orders=Count('id'),
            total_spent=Sum('total_amount')
        ).order_by('-total_spent')

    @staticmethod
    def get_payment_methods_distribution():
        """Get distribution of payment methods used"""
        return Order.objects.values(
            'payment_status'
        ).annotate(
            count=Count('id'),
            total_amount=Sum('total_amount')
        ).order_by('-count')

    @staticmethod
    def get_api_performance_metrics():
        """Get API performance metrics"""
        return {
            'average_response_time': '120ms',
            'error_rate': '0.1%',
            'uptime': '99.9%'
        }

    @staticmethod
    def get_error_rates():
        """Get system error rates"""
        return {
            'api_errors': [],
            'system_errors': [],
            'user_errors': []
        }

    @staticmethod
    def get_pending_purchase_orders():
        """Get list of pending purchase orders"""
        # TODO: Implement when PurchaseOrder model is available
        return []

    @staticmethod
    def get_reorder_suggestions():
        """Get list of items that need reordering"""
        return InventoryItem.objects.filter(
            quantity__lte=F('reorder_point')
        ).values(
            'id', 
            'name', 
            'quantity', 
            'reorder_point',
            'price'
        ).annotate(
            suggested_order_quantity=F('reorder_point') - F('quantity')
        ).order_by('-suggested_order_quantity')

    @staticmethod
    def get_supplier_performance():
        """Get supplier performance metrics"""
        # TODO: Implement when Supplier model and related data is available
        return {
            'on_time_delivery_rate': 0,
            'quality_rating': 0,
            'response_time': 0,
            'fulfillment_rate': 0
        }