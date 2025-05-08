from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.repositories.dashboard_repository import DashboardRepository
from datetime import datetime, timedelta

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    repository = DashboardRepository
    service = DashboardService(repository)

    def get(self, request):
        role = request.user.role
        time_range = request.query_params.get('time_range', 'week')  # week, month, year
        
        # Common data for all roles
        common_data = {
            "last_login": request.user.last_login,
            "notifications": self.service.get_user_notifications(request.user.id),
            "recent_activities": self.service.get_recent_activities(request.user.id)
        }

        if role == "admin":
            data = {
                **common_data,
                "overview": {
                    "total_users": self.service.get_total_users(),
                    "active_users": self.service.get_active_users(),
                    "total_revenue": self.service.get_total_revenue(time_range),
                    "total_orders": self.service.get_total_orders(time_range)
                },
                "user_statistics": {
                    "new_users": self.service.get_new_users_stats(time_range),
                    "user_types": self.service.get_user_type_distribution(),
                    "active_shops": self.service.get_active_shops_count()
                },
                "financial_metrics": {
                    "revenue_trends": self.service.get_revenue_trends(time_range),
                    "top_performing_products": self.service.get_top_products(time_range),
                    "payment_methods_distribution": self.service.get_payment_methods_stats()
                },
                "system_health": {
                    "system_status": self.service.get_system_health(),
                    "api_performance": self.service.get_api_performance_metrics(),
                    "error_rates": self.service.get_error_rates()
                }
            }
        
        elif role == "inventory_manager":
            data = {
                **common_data,
                "inventory_summary": {
                    "total_items": self.service.get_total_inventory_items(),
                    "low_stock_items": self.service.get_low_stock_items(),
                    "expiring_soon": self.service.get_expiring_stock(),
                    "stock_value": self.service.get_total_stock_value()
                },
                "inventory_metrics": {
                    "stock_movements": self.service.get_stock_movements(time_range),
                    "top_moving_items": self.service.get_top_moving_items(),
                    "stock_alerts": self.service.get_stock_alerts()
                },
                "procurement_insights": {
                    "pending_orders": self.service.get_pending_purchase_orders(),
                    "reorder_suggestions": self.service.get_reorder_suggestions(),
                    "supplier_performance": self.service.get_supplier_performance()
                }
            }
        
        elif role == "shop_owner":
            data = {
                **common_data,
                "shop_performance": {
                    "daily_sales": self.service.get_shop_sales(request.user.id, time_range),
                    "popular_products": self.service.get_shop_popular_products(request.user.id),
                    "customer_satisfaction": self.service.get_customer_satisfaction(request.user.id)
                },
                "order_metrics": {
                    "pending_orders": self.service.get_shop_pending_orders(request.user.id),
                    "order_status_distribution": self.service.get_order_status_distribution(request.user.id),
                    "delivery_performance": self.service.get_delivery_performance(request.user.id)
                },
                "financial_overview": {
                    "revenue_summary": self.service.get_shop_revenue_summary(request.user.id, time_range),
                    "payment_analytics": self.service.get_shop_payment_analytics(request.user.id),
                    "profit_margins": self.service.get_shop_profit_margins(request.user.id)
                }
            }
        
        elif role == "farmer":
            data = {
                **common_data,
                "crop_overview": {
                    "active_crops": self.service.get_farmer_active_crops(request.user.id),
                    "harvest_schedule": self.service.get_harvest_schedule(request.user.id),
                    "crop_health": self.service.get_crop_health_metrics(request.user.id)
                },
                "market_insights": {
                    "current_prices": self.service.get_market_prices(),
                    "demand_forecast": self.service.get_demand_forecast(),
                    "best_selling_crops": self.service.get_best_selling_crops()
                },
                "sales_analytics": {
                    "sales_history": self.service.get_farmer_sales_history(request.user.id, time_range),
                    "buyer_insights": self.service.get_farmer_buyer_insights(request.user.id),
                    "revenue_trends": self.service.get_farmer_revenue_trends(request.user.id, time_range)
                }
            }

        return Response(data, status=status.HTTP_200_OK)