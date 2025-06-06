from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.repositories.dashboard_repository import DashboardRepository
from datetime import datetime, timedelta
from utils import setup_logger

logger = setup_logger(__name__)

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    repository = DashboardRepository
    service = DashboardService(repository)

    def get(self, request):
        try:
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
                try:
                    metrics.update({
                        "production_metrics": {
                            "dairy": {
                                "daily_production": self.service.get_dairy_production_summary(user.id, time_range),
                                "inventory_status": self.service.get_dairy_inventory_status(user.id),
                                "quality_metrics": self.service.get_dairy_quality_metrics(user.id, time_range)
                            }
                        },
                        "inventory_metrics": {
                            "current_stock": self.service.get_farmer_inventory(user.id),
                            "storage_utilization": self.service.get_storage_utilization(user.id),
                            "expiring_soon": self.service.get_expiring_products(user.id)
                        },
                        "market_metrics": {
                            "market_prices": self.service.get_market_prices(),
                            "demand_forecast": self.service.get_demand_forecast(),
                            "best_selling_products": self.service.get_best_selling_products(user.id),
                            "competitor_analysis": self.service.get_competitor_analysis()
                        },
                        "sales_metrics": {
                            "sales_summary": self.service.get_farmer_sales_summary(user.id, time_range),
                            "revenue_trends": self.service.get_farmer_revenue_trends(user.id, time_range),
                            "buyer_insights": self.service.get_farmer_buyer_insights(user.id),
                            "payment_statistics": self.service.get_payment_statistics(user.id, time_range)
                        },
                        "operational_metrics": {
                            "equipment_status": self.service.get_equipment_status(user.id),
                            "maintenance_schedule": self.service.get_maintenance_schedule(user.id),
                            "resource_utilization": self.service.get_resource_utilization(user.id)
                        },
                        "financial_metrics": {
                            "profit_loss": self.service.get_profit_loss_summary(user.id, time_range),
                            "expenses": self.service.get_expense_breakdown(user.id, time_range),
                            "outstanding_payments": self.service.get_outstanding_payments(user.id)
                        }
                    })
                except Exception as e:
                    logger.error(f"Error getting farmer metrics: {str(e)}")
                    metrics.update({
                        "production_metrics": {},
                        "inventory_metrics": {},
                        "market_metrics": {},
                        "sales_metrics": {},
                        "operational_metrics": {},
                        "financial_metrics": {}
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
            
            # Mock data for testing
            mock_data = {
                "production_metrics": {
                    "dairy": {
                        "daily_production": {"milk": 500, "cheese": 50, "butter": 20},
                        "inventory_status": {"in_stock": 1200, "sold": 800},
                        "quality_metrics": {"grade_a": "85%", "grade_b": "12%", "grade_c": "3%"}
                    }
                },
                "inventory_metrics": {
                    "current_stock": 2000,
                    "storage_utilization": "75%",
                    "expiring_soon": 150
                },
                "market_metrics": {
                    "market_prices": {"milk": 35, "cheese": 250, "butter": 180},
                    "demand_forecast": "high",
                    "best_selling_products": ["Fresh Milk", "Cheese", "Yogurt"],
                    "competitor_analysis": {"market_share": "15%", "price_comparison": "competitive"}
                },
                "sales_metrics": {
                    "sales_summary": {"total_sales": 50000, "top_product": "Fresh Milk"},
                    "revenue_trends": {"monthly_growth": "5%", "yearly_growth": "10%"},
                    "buyer_insights": {"repeat_buyers": 300, "new_buyers": 150},
                    "payment_statistics": {"pending_payments": 2000, "received_payments": 48000}
                },
                "operational_metrics": {
                    "equipment_status": {"operational": 10, "maintenance_needed": 2},
                    "maintenance_schedule": {"next_maintenance": "2023-12-01"},
                    "resource_utilization": {"water_usage": "5000L", "feed_usage": "2000kg"}
                },
                "financial_metrics": {
                    "profit_loss": {"profit": 15000, "loss": 5000},
                    "expenses": {"operational_expenses": 3000, "maintenance_expenses": 2000},
                    "outstanding_payments": 1000
                }
            }

            return Response({
                "status": True,
                "message": "Dashboard summary retrieved successfully.",
                "data": mock_data,
                "timestamp": datetime.now().isoformat(),
                "time_range": time_range
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "message": f"Failed to retrieve dashboard summary",
                "timestamp": datetime.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)