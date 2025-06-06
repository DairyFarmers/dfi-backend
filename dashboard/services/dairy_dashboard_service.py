from datetime import datetime, timedelta
from django.utils import timezone
from utils import setup_logger

logger = setup_logger(__name__)

class DairyDashboardService:
    def __init__(self, repository):
        self.repository = repository

    def get_dairy_dashboard_metrics(self, farmer_id, time_range='week'):
        """Get comprehensive dairy dashboard metrics"""
        try:
            production_summary = self.repository.get_dairy_production_summary(
                farmer_id, 
                time_range
            )
            inventory_status = self.repository.get_dairy_inventory_status(
                farmer_id
            )
            revenue_metrics = self.repository.get_dairy_revenue_metrics(
                farmer_id, 
                time_range
            )

            return {
                "production_metrics": {
                    "summary": production_summary,
                    "total_production": sum(
                        item['total_quantity'] for item in production_summary
                    ),
                    "quality_metrics": {
                        item['product_type']: item['avg_quality'] 
                        for item in production_summary
                    }
                },
                "inventory_metrics": {
                    "current_stock": inventory_status,
                    "expiring_soon": sum(
                        item['expiring_soon'] for item in inventory_status
                    ),
                    "storage_utilization": self._calculate_storage_utilization(
                        inventory_status
                    )
                },
                "revenue_metrics": {
                    "daily_revenue": list(revenue_metrics),
                    "total_revenue": sum(
                        item['daily_revenue'] for item in revenue_metrics
                    ),
                    "product_performance": self._get_product_performance(
                        farmer_id, 
                        time_range
                    )
                }
            }
        except Exception as e:
            logger.error(f"Error getting dairy dashboard metrics: {str(e)}")
            return {
                "production_metrics": {},
                "inventory_metrics": {},
                "revenue_metrics": {}
            }

    def _calculate_storage_utilization(self, inventory_status):
        """Calculate storage utilization percentage"""
        # Implement storage capacity calculation logic
        return {
            "used_capacity": sum(
                item['total_quantity'] for item in inventory_status
            ),
            "total_capacity": 1000,  # Example fixed capacity
            "utilization_percentage": 0  # Calculate based on actual capacity
        }

    def _get_product_performance(self, farmer_id, time_range):
        """Get performance metrics for each dairy product"""
        # Implement product-specific performance metrics
        return {
            "best_selling": self.repository.get_best_selling_products(
                farmer_id,
                category='dairy'
            ),
            "highest_revenue": self.repository.get_highest_revenue_products(
                farmer_id,
                category='dairy'
            )
        }