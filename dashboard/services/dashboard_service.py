from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg
from django.utils import timezone

class DashboardService:
    def __init__(self, repository):
        self.repository = repository

    # Common Methods
    def get_user_notifications(self, user_id):
        return self.repository.get_user_notifications(user_id)

    def get_recent_activities(self, user_id):
        return self.repository.get_recent_activities(user_id)

    # Admin Dashboard Methods
    def get_total_users(self):
        return self.repository.get_total_users()

    def get_active_users(self):
        return self.repository.get_active_users()

    def get_total_revenue(self, time_range):
        return self.repository.get_total_revenue(time_range)

    def get_total_orders(self, time_range):
        return self.repository.get_total_orders(time_range)

    def get_pending_orders(self):
        return self.repository.get_pending_orders()

    def get_new_users_stats(self, time_range):
        return self.repository.get_new_users_stats(time_range)

    def get_user_type_distribution(self):
        return self.repository.get_user_type_distribution()

    def get_active_shops_count(self):
        return self.repository.get_active_shops_count()

    def get_revenue_trends(self, time_range):
        return self.repository.get_revenue_trends(time_range)

    def get_top_products(self, time_range):
        return self.repository.get_top_products(time_range)

    def get_payment_methods_stats(self):
        return self.repository.get_payment_methods_distribution()

    def get_system_health(self):
        return self.repository.get_system_health()

    def get_api_performance_metrics(self):
        return self.repository.get_api_performance_metrics()

    def get_error_rates(self):
        return self.repository.get_error_rates()

    # Inventory Manager Methods
    def get_total_inventory_items(self):
        return self.repository.get_total_inventory_items()

    def get_low_stock_items(self):
        return self.repository.get_low_stock_items()

    def get_expiring_stock(self):
        return self.repository.get_expiring_stock()

    def get_total_stock_value(self):
        return self.repository.get_total_stock_value()

    def get_stock_movements(self, time_range):
        return self.repository.get_stock_movements(time_range)

    def get_top_moving_items(self):
        return self.repository.get_top_moving_items()

    def get_stock_alerts(self):
        return self.repository.get_stock_alerts()

    def get_pending_purchase_orders(self):
        return self.repository.get_pending_purchase_orders()

    def get_reorder_suggestions(self):
        return self.repository.get_reorder_suggestions()

    def get_supplier_performance(self):
        return self.repository.get_supplier_performance()

    # Shop Owner Methods
    def get_shop_sales(self, shop_owner_id, time_range):
        return self.repository.get_shop_sales(shop_owner_id, time_range)

    def get_shop_popular_products(self, shop_owner_id):
        return self.repository.get_shop_popular_products(shop_owner_id)

    def get_customer_satisfaction(self, shop_owner_id):
        return self.repository.get_customer_satisfaction(shop_owner_id)

    def get_shop_pending_orders(self, shop_owner_id):
        return self.repository.get_shop_pending_orders(shop_owner_id)

    def get_order_status_distribution(self, shop_owner_id=None):
        return self.repository.get_order_status_distribution(shop_owner_id)

    def get_delivery_performance(self, shop_owner_id):
        return self.repository.get_delivery_performance(shop_owner_id)

    def get_shop_revenue_summary(self, shop_owner_id, time_range):
        return self.repository.get_shop_revenue_summary(shop_owner_id, time_range)

    def get_shop_payment_analytics(self, shop_owner_id):
        return self.repository.get_shop_payment_analytics(shop_owner_id)

    def get_shop_profit_margins(self, shop_owner_id):
        return self.repository.get_shop_profit_margins(shop_owner_id)

    # Farmer Methods
    def get_farmer_active_crops(self, farmer_id):
        return self.repository.get_farmer_active_crops(farmer_id)

    def get_harvest_schedule(self, farmer_id):
        return self.repository.get_harvest_schedule(farmer_id)

    def get_crop_health_metrics(self, farmer_id):
        return self.repository.get_crop_health_metrics(farmer_id)

    def get_market_prices(self):
        return self.repository.get_market_prices()

    def get_demand_forecast(self):
        return self.repository.get_demand_forecast()

    def get_best_selling_crops(self):
        return self.repository.get_best_selling_crops()

    def get_farmer_sales_history(self, farmer_id, time_range):
        return self.repository.get_farmer_sales_history(farmer_id, time_range)

    def get_farmer_buyer_insights(self, farmer_id):
        return self.repository.get_farmer_buyer_insights(farmer_id)

    def get_farmer_revenue_trends(self, farmer_id, time_range):
        return self.repository.get_farmer_revenue_trends(farmer_id, time_range)

    def get_dashboard_summary(self, time_range='week'):
        """Get complete dashboard summary"""
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
    
    def get_user_statistics(self):
        return self.repository.get_user_statistics()

    def get_stock_summary(self):
        return self.repository.get_stock_summary()

    def get_orders_overview(self):
        return self.repository.get_orders_overview()

    def get_sales_graph_data(self):
        return self.repository.get_sales_graph_data()