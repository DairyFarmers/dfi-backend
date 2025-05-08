from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from users.models.user import User
from inventories.models.inventory_item import InventoryItem
from orders.models.order import Order
from orders.models.order_item import OrderItem
from users.models.user_activity_log import UserActivityLog

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
        return UserActivityLog.objects.filter(
            user_id=user_id
        ).order_by('-timestamp')[:10]

    # Admin Dashboard Methods
    @staticmethod
    def get_total_users():
        return User.objects.count()

    @staticmethod
    def get_active_users_count():
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return User.objects.filter(last_login__gte=thirty_days_ago).count()

    @staticmethod
    def get_total_revenue(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            created_at__gte=start_date,
            status='completed'
        ).aggregate(total_revenue=Sum('total_amount'))

    @staticmethod
    def get_total_orders(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(created_at__gte=start_date).count()

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
    def get_revenue_trends(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            created_at__gte=start_date,
            status='completed'
        ).values('created_at__date').annotate(
            daily_revenue=Sum('total_amount')
        ).order_by('created_at__date')

    @staticmethod
    def get_top_products(time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return OrderItem.objects.filter(
            order__created_at__gte=start_date
        ).values('product__name').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('unit_price'))
        ).order_by('-total_revenue')[:10]

    @staticmethod
    def get_payment_methods_distribution():
        return Order.objects.values('payment_method').annotate(
            count=Count('id'),
            total_amount=Sum('total_amount')
        )

    @staticmethod
    def get_system_health_metrics():
        # Implement system health checks here
        return {
            'system_status': 'healthy',
            'database_status': 'connected',
            'cache_status': 'operational'
        }

    @staticmethod
    def get_api_performance_metrics():
        # Implement API performance metrics here
        return {
            'average_response_time': '120ms',
            'error_rate': '0.1%',
            'uptime': '99.9%'
        }

    @staticmethod
    def get_error_rates():
        # Implement error rate tracking here
        return {
            'api_errors': [],
            'system_errors': [],
            'user_errors': []
        }

    # Inventory Manager Methods
    @staticmethod
    def get_total_inventory_items():
        return InventoryItem.objects.aggregate(
            total_items=Count('id'),
            total_quantity=Sum('quantity')
        )

    @staticmethod
    def get_low_stock_items():
        return InventoryItem.objects.filter(
            quantity__lte=F('reorder_level')
        ).select_related('product')

    @staticmethod
    def get_expiring_stock():
        thirty_days_from_now = timezone.now() + timedelta(days=30)
        return InventoryItem.objects.filter(
            expiry_date__lte=thirty_days_from_now
        ).select_related('product')

    @staticmethod
    def get_total_stock_value():
        return InventoryItem.objects.aggregate(
            total_value=Sum(F('quantity') * F('unit_price'))
        )

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
            Q(quantity__lte=F('reorder_level')) |
            Q(expiry_date__lte=timezone.now() + timedelta(days=30))
        ).select_related('product')

    # Shop Owner Methods
    @staticmethod
    def get_shop_sales(shop_owner_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            shop_owner_id=shop_owner_id,
            created_at__gte=start_date
        ).values('created_at__date').annotate(
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
    def get_order_status_distribution(shop_owner_id):
        return Order.objects.filter(
            shop_owner_id=shop_owner_id
        ).values('status').annotate(count=Count('id'))

    # Farmer Methods
    @staticmethod
    def get_farmer_active_crops(farmer_id):
        # TODO: Implement when Crop model is available
        return []

    @staticmethod
    def get_harvest_schedule(farmer_id):
        # TODO: Implement when Crop model is available
        return []

    @staticmethod
    def get_crop_health_metrics(farmer_id):
        # TODO: Implement when CropHealth model is available
        return []

    @staticmethod
    def get_market_prices():
        # TODO: Implement when MarketPrice model is available
        return []

    @staticmethod
    def get_demand_forecast():
        # TODO: Implement when Demand model is available
        return []

    @staticmethod
    def get_best_selling_crops():
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return OrderItem.objects.filter(
            order__created_at__gte=thirty_days_ago,
            product__category='crop'
        ).values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:10]

    @staticmethod
    def get_farmer_sales_history(farmer_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            farmer_id=farmer_id,
            created_at__gte=start_date
        ).values('created_at__date').annotate(
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
    def get_farmer_revenue_trends(farmer_id, time_range):
        start_date = DashboardRepository.get_time_range_filter(time_range)
        return Order.objects.filter(
            farmer_id=farmer_id,
            created_at__gte=start_date
        ).values('created_at__date').annotate(
            revenue=Sum('total_amount')
        ).order_by('created_at__date')