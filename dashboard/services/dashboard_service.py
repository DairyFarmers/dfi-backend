from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from exceptions import ServiceException, RepositoryException
from utils import setup_logger

logger = setup_logger(__name__)

class DashboardService:
    def __init__(self, repository):
        self.repository = repository
        self.logger = setup_logger(__name__)

    # Common Methods
    def get_user_notifications(self, user_id):
        try:
            self.logger.info(f"Fetching notifications for user {user_id}")
            return self.repository.get_user_notifications(user_id)
        except RepositoryException as e:
            self.logger.error(f"Error fetching notifications for user {user_id}: {str(e)}")
            raise ServiceException(f"Error fetching notifications: {str(e)}")

    def get_recent_activities(self, user_id):
        try:
            self.logger.info(f"Fetching recent activities for user {user_id}")
            return self.repository.get_recent_activities(user_id)
        except RepositoryException as e:
            self.logger.error(f"Error fetching recent activities for user {user_id}: {str(e)}")
            raise ServiceException(f"Error fetching recent activities: {str(e)}")

    # Admin Dashboard Methods
    def get_total_users(self):
        try:
            self.logger.info("Fetching total users")
            return self.repository.get_total_users()
        except RepositoryException as e:
            self.logger.error(f"Error fetching total users: {str(e)}")
            raise ServiceException(f"Error fetching total users: {str(e)}")

    def get_active_users(self):
        try:
            self.logger.info("Fetching active users")
            return self.repository.get_active_users()
        except RepositoryException as e:
            self.logger.error(f"Error fetching active users: {str(e)}")
            raise ServiceException(f"Error fetching active users: {str(e)}")

    def get_total_revenue(self, time_range):
        try:
            self.logger.info(f"Fetching total revenue for time range: {time_range}")
            return self.repository.get_total_revenue(time_range)
        except RepositoryException as e:
            self.logger.error(f"Error fetching total revenue: {str(e)}")
            raise ServiceException(f"Error fetching total revenue: {str(e)}")

    def get_total_orders(self, time_range):
        try:
            self.logger.info(f"Fetching total orders for time range: {time_range}")
            return self.repository.get_total_orders(time_range)
        except RepositoryException as e:
            self.logger.error(f"Error fetching total orders: {str(e)}")
            raise ServiceException(f"Error fetching total orders: {str(e)}")

    def get_pending_orders(self):
        try:
            self.logger.info("Fetching pending orders")
            return self.repository.get_pending_orders()
        except RepositoryException as e:
            self.logger.error(f"Error fetching pending orders: {str(e)}")
            raise ServiceException(f"Error fetching pending orders: {str(e)}")

    def get_new_users_stats(self, time_range):
        try:
            self.logger.info(f"Fetching new users stats for time range: {time_range}")
            return self.repository.get_new_users_stats(time_range)
        except RepositoryException as e:
            self.logger.error(f"Error fetching new users stats: {str(e)}")
            raise ServiceException(f"Error fetching new users stats: {str(e)}")

    def get_user_type_distribution(self):
        try:
            self.logger.info("Fetching user type distribution")
            return self.repository.get_user_type_distribution()
        except RepositoryException as e:
            self.logger.error(f"Error fetching user type distribution: {str(e)}")
            raise ServiceException(f"Error fetching user type distribution: {str(e)}")

    def get_active_shops_count(self):
        try:
            self.logger.info("Fetching active shops count")
            return self.repository.get_active_shops_count()
        except RepositoryException as e:
            self.logger.error(f"Error fetching active shops count: {str(e)}")
            raise ServiceException(f"Error fetching active shops count: {str(e)}")

    def get_revenue_trends(self, time_range):
        try:
            self.logger.info(f"Fetching revenue trends for time range: {time_range}")
            return self.repository.get_revenue_trends(time_range)
        except RepositoryException as e:
            self.logger.error(f"Error fetching revenue trends: {str(e)}")
            raise ServiceException(f"Error fetching revenue trends: {str(e)}")

    def get_top_products(self, time_range):
        try:
            self.logger.info(f"Fetching top products for time range: {time_range}")
            return self.repository.get_top_products(time_range)
        except RepositoryException as e:
            self.logger.error(f"Error fetching top products: {str(e)}")
            raise ServiceException(f"Error fetching top products: {str(e)}")

    def get_payment_methods_stats(self):
        try:
            self.logger.info("Fetching payment methods distribution")
            return self.repository.get_payment_methods_distribution()
        except RepositoryException as e:
            self.logger.error(f"Error fetching payment methods stats: {str(e)}")
            raise ServiceException(f"Error fetching payment methods stats: {str(e)}")

    def get_system_health(self):
        try:
            self.logger.info("Fetching system health metrics")
            return self.repository.get_system_health()
        except RepositoryException as e:
            self.logger.error(f"Error fetching system health: {str(e)}")
            raise ServiceException(f"Error fetching system health: {str(e)}")

    def get_api_performance_metrics(self):
        try:
            self.logger.info("Fetching API performance metrics")
            return self.repository.get_api_performance_metrics()
        except RepositoryException as e:
            self.logger.error(f"Error fetching API performance metrics: {str(e)}")
            raise ServiceException(f"Error fetching API performance metrics: {str(e)}")

    def get_error_rates(self):
        try:
            self.logger.info("Fetching error rates")
            return self.repository.get_error_rates()
        
        except RepositoryException as e:
            raise ServiceException(f"Error fetching error rates: {str(e)}")

    # Inventory Manager Methods
    def get_total_inventory_items(self):
        try:
            return self.repository.get_total_inventory_items()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching total inventory items: {str(e)}")

    def get_low_stock_items(self):
        try:
            return self.repository.get_low_stock_items()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching low stock items: {str(e)}")

    def get_expiring_stock(self):
        try:
            return self.repository.get_expiring_stock()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching expiring stock: {str(e)}")

    def get_total_stock_value(self):
        try:
            return self.repository.get_total_stock_value()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching total stock value: {str(e)}")

    def get_stock_movements(self, time_range):
        try:
            return self.repository.get_stock_movements(time_range)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching stock movements: {str(e)}")

    def get_top_moving_items(self):
        try:
            return self.repository.get_top_moving_items()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching top moving items: {str(e)}")

    # Stock Methods
    def get_stock_alerts(self):
        try:
            return self.repository.get_stock_alerts()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching stock alerts: {str(e)}")

    def get_pending_purchase_orders(self):
        try:
            return self.repository.get_pending_purchase_orders()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching pending purchase orders: {str(e)}")

    def get_reorder_suggestions(self):
        try:
            return self.repository.get_reorder_suggestions()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching reorder suggestions: {str(e)}")

    def get_supplier_performance(self):
        try:
            return self.repository.get_supplier_performance()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching supplier performance: {str(e)}")

    # Shop Owner Methods
    def get_shop_sales(self, shop_owner_id, time_range):
        try:
            return self.repository.get_shop_sales(shop_owner_id, time_range)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching shop sales: {str(e)}")

    def get_shop_popular_products(self, shop_owner_id):
        try:
            return self.repository.get_shop_popular_products(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching shop popular products: {str(e)}")

    def get_customer_satisfaction(self, shop_owner_id):
        try:
            return self.repository.get_customer_satisfaction(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching customer satisfaction: {str(e)}")

    def get_shop_pending_orders(self, shop_owner_id):
        try:
            return self.repository.get_shop_pending_orders(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching shop pending orders: {str(e)}")

    def get_order_status_distribution(self, shop_owner_id=None):
        try:
            return self.repository.get_order_status_distribution(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching order status distribution: {str(e)}")

    def get_delivery_performance(self, shop_owner_id):
        try:
            return self.repository.get_delivery_performance(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching delivery performance: {str(e)}")

    def get_shop_revenue_summary(self, shop_owner_id, time_range):
        try:
            return self.repository.get_shop_revenue_summary(shop_owner_id, time_range)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching shop revenue summary: {str(e)}")

    def get_shop_payment_analytics(self, shop_owner_id):
        try:
            return self.repository.get_shop_payment_analytics(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching shop payment analytics: {str(e)}")

    def get_shop_profit_margins(self, shop_owner_id):
        try:
            return self.repository.get_shop_profit_margins(shop_owner_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching shop profit margins: {str(e)}")

    # Farmer Methods
    def get_farmer_active_crops(self, farmer_id):
        try:
            return self.repository.get_farmer_active_crops(farmer_id) or {
                'count': 0,
                'crops': []
            }
        except RepositoryException as e:
            logger.error(f"Error getting farmer active crops: {str(e)}")
            return {
                'count': 0,
                'crops': []
            }


    def get_harvest_schedule(self, farmer_id):
        try:
            return self.repository.get_harvest_schedule(farmer_id) or {
                'upcoming': [],
                'ongoing': []
            }
        except Exception as e:
            logger.error(f"Error getting harvest schedule: {str(e)}")
            return {
                'upcoming': [],
                'ongoing': []
            }

    def get_crop_health_metrics(self, farmer_id):
        """Get crop health metrics for a farmer"""
        try:
            return self.repository.get_crop_health_metrics(farmer_id) or {
                'healthy': 0,
                'at_risk': 0,
                'needs_attention': 0
            }
        except Exception as e:
            logger.error(f"Error getting crop health metrics: {str(e)}")
            return {
                'healthy': 0,
                'at_risk': 0,
                'needs_attention': 0
            }

    def get_market_prices(self):
        try:
            return self.repository.get_market_prices()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching market prices: {str(e)}")

    def get_demand_forecast(self):
        try:
            return self.repository.get_demand_forecast()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching demand forecast: {str(e)}")

    def get_best_selling_crops(self):
        try:
            return self.repository.get_best_selling_crops()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching best selling crops: {str(e)}")

    def get_farmer_sales_history(self, farmer_id, time_range):
        try:
            return self.repository.get_farmer_sales_history(farmer_id, time_range)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching farmer sales history: {str(e)}")

    def get_farmer_buyer_insights(self, farmer_id):
        try:
            return self.repository.get_farmer_buyer_insights(farmer_id)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching farmer buyer insights: {str(e)}")

    def get_farmer_revenue_trends(self, farmer_id, time_range):
        try:
            return self.repository.get_farmer_revenue_trends(farmer_id, time_range)
        except RepositoryException as e:
            raise ServiceException(f"Error fetching farmer revenue trends: {str(e)}")

    def get_dashboard_summary(self, time_range='week'):
        """Get complete dashboard summary"""
        try:
            return {
                "total_orders": self.repository.get_total_orders(time_range),
                "total_revenue": self.repository.get_total_revenue(time_range),
                "pending_orders": self.repository.get_pending_orders(),
                "inventory_status": {
                    "total_items": self.repository.get_total_inventory_items(),
                    "low_stock_items": self.repository.get_low_stock_items(),
                    "stock_value": self.repository.get_total_stock_value()
                },
                "order_metrics": {
                    "status_distribution": self.repository.get_order_status_distribution(),
                    "recent_orders": self.repository.get_total_orders(time_range)
                }
            }
        except RepositoryException as e:
            raise ServiceException(f"Error fetching dashboard summary: {str(e)}")
    
    def get_user_statistics(self):
        try:
            return self.repository.get_user_statistics()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching user statistics: {str(e)}")

    def get_stock_summary(self):
        try:
            return self.repository.get_stock_summary()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching stock summary: {str(e)}")

    def get_orders_overview(self):
        try:
            return self.repository.get_orders_overview()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching orders overview: {str(e)}")

    def get_sales_graph_data(self):
        try:
            return self.repository.get_sales_graph_data()
        except RepositoryException as e:
            raise ServiceException(f"Error fetching sales graph data: {str(e)}")