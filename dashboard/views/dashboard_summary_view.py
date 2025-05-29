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
        time_range = request.query_params.get('time_range', 'week')
        user = request.user
        role_name = user.role.name if user.role else None
        
        # Common data for all users
        common_data = {
            "last_login": user.last_login,
            "notifications": self.service.get_user_notifications(user.id),
            "recent_activities": self.service.get_recent_activities(user.id)
        }

        # Initialize metrics containers
        metrics = {}

        # Admin Dashboard
        if role_name == 'admin':
            metrics.update({
                "system_metrics": {
                    "total_users": self.service.get_total_users(),
                    "active_users": self.service.get_active_users(),
                    "system_health": self.service.get_system_health()
                },
                "financial_metrics": {
                    "total_revenue": self.service.get_total_revenue(time_range),
                    "revenue_trends": self.service.get_revenue_trends(time_range)
                },
                "inventory_metrics": {
                    "total_items": self.service.get_total_inventory_items(),
                    "low_stock_items": self.service.get_low_stock_items(),
                    "stock_value": self.service.get_total_stock_value()
                },
                "order_metrics": {
                    "total_orders": self.service.get_total_orders(time_range),
                    "pending_orders": self.service.get_pending_orders(),
                    "order_status_distribution": self.service.get_order_status_distribution()
                }
            })

        # Inventory Manager Dashboard
        elif role_name == 'inventory_manager':
            metrics.update({
                "inventory_metrics": {
                    "total_items": self.service.get_total_inventory_items(),
                    "low_stock_items": self.service.get_low_stock_items(),
                    "stock_value": self.service.get_total_stock_value(),
                    "expiring_stock": self.service.get_expiring_stock(),
                    "stock_movements": self.service.get_stock_movements(time_range),
                    "top_moving_items": self.service.get_top_moving_items()
                },
                "order_metrics": {
                    "pending_orders": self.service.get_pending_orders(),
                    "order_status_distribution": self.service.get_order_status_distribution()
                },
                "supplier_metrics": {
                    "pending_purchase_orders": self.service.get_pending_purchase_orders(),
                    "reorder_suggestions": self.service.get_reorder_suggestions(),
                    "supplier_performance": self.service.get_supplier_performance()
                }
            })

        # Sales Representative Dashboard
        elif role_name == 'sales_representative':
            metrics.update({
                "sales_metrics": {
                    "sales_overview": self.service.get_user_sales(user.id, time_range),
                    "popular_products": self.service.get_user_popular_products(user.id),
                    "revenue_summary": self.service.get_user_revenue_summary(user.id, time_range)
                },
                "order_metrics": {
                    "pending_orders": self.service.get_pending_orders(),
                    "order_status_distribution": self.service.get_order_status_distribution(shop_owner_id=user.id)
                },
                "inventory_overview": {
                    "available_items": self.service.get_total_inventory_items(),
                    "low_stock_alerts": self.service.get_low_stock_items()
                }
            })

        # Farmer Dashboard
        elif role_name == 'farmer':
            metrics.update({
                "crop_metrics": {
                    "active_crops": self.service.get_farmer_active_crops(user.id),
                    "harvest_schedule": self.service.get_harvest_schedule(user.id),
                    "crop_health": self.service.get_crop_health_metrics(user.id)
                },
                "market_metrics": {
                    "market_prices": self.service.get_market_prices(),
                    "demand_forecast": self.service.get_demand_forecast(),
                    "best_selling_crops": self.service.get_best_selling_crops()
                },
                "sales_metrics": {
                    "sales_history": self.service.get_farmer_sales_history(user.id, time_range),
                    "buyer_insights": self.service.get_farmer_buyer_insights(user.id),
                    "revenue_trends": self.service.get_farmer_revenue_trends(user.id, time_range)
                }
            })

        # B2B Dashboard
        elif role_name == 'b2b':
            metrics.update({
                "order_metrics": {
                    "pending_orders": self.service.get_pending_orders(),
                    "order_status_distribution": self.service.get_order_status_distribution(shop_owner_id=user.id)
                },
                "inventory_overview": {
                    "available_items": self.service.get_total_inventory_items(),
                    "low_stock_alerts": self.service.get_low_stock_items()
                },
                "market_metrics": {
                    "market_prices": self.service.get_market_prices(),
                    "demand_forecast": self.service.get_demand_forecast()
                }
            })

        # Combine all data
        data = {
            **common_data,
            **metrics
        }

        return Response({
            "status": True,
            "message": "Dashboard summary retrieved successfully.",
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "time_range": time_range
        }, status=status.HTTP_200_OK)