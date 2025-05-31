from typing import List, Optional
from django.db.models import Q
from reports.models.report import Report
from orders.models import Order
from inventories.models import InventoryItem
from users.models import User
from .base_repository import BaseRepository
from django.db import DatabaseError
from exceptions import DatabaseException

class ReportRepository(BaseRepository):
    def __init__(self):
        super().__init__(Report)
        self.order_model = Order
        self.inventory_model = InventoryItem
        self.user_model = User

    def create_report(self, data: dict) -> Report:
        """Create a new report"""
        try:
            return self.model.objects.create(**data)
        except DatabaseError as e:
            raise DatabaseException(f"Failed to create report: {str(e)}")

    def get_reports_by_user(self, user_id: str, filters: Optional[dict] = None) -> List[Report]:
        """Get all reports for a specific user with optional filtering"""
        try:
            queryset = self.model.objects.filter(generated_by_id=user_id)
            
            if filters:
                if 'report_type' in filters:
                    queryset = queryset.filter(report_type=filters['report_type'])
                if 'status' in filters:
                    queryset = queryset.filter(status=filters['status'])
                if 'date_from' in filters:
                    queryset = queryset.filter(generated_at__gte=filters['date_from'])
                if 'date_to' in filters:
                    queryset = queryset.filter(generated_at__lte=filters['date_to'])

            return queryset.select_related('generated_by').order_by('-generated_at')
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch reports: {str(e)}")

    def get_report_data(self, report_type: str, date_from: str, date_to: str) -> dict:
        """Get data for report generation based on type"""
        try:
            if report_type == 'sales':
                return self._get_sales_data(date_from, date_to)
            elif report_type == 'inventory':
                return self._get_inventory_data(date_from, date_to)
            elif report_type == 'user_activity':
                return self._get_user_activity_data(date_from, date_to)
            else:
                raise ValueError(f"Invalid report type: {report_type}")
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch report data: {str(e)}")

    def _get_sales_data(self, date_from: str, date_to: str) -> dict:
        """Get sales related data"""
        try:
            orders = self.order_model.objects.filter(
                created_at__range=[date_from, date_to]
            ).select_related('customer')
            
            return {
                'total_orders': orders.count(),
                'total_revenue': sum(order.total_amount for order in orders),
                'orders': orders
            }
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch sales data: {str(e)}")

    def _get_inventory_data(self, date_from: str, date_to: str) -> dict:
        """Get inventory related data"""
        try:
            inventory_items = self.inventory_model.objects.filter(
                Q(created_at__range=[date_from, date_to]) |
                Q(updated_at__range=[date_from, date_to])
            )
            
            return {
                'total_items': inventory_items.count(),
                'low_stock_items': inventory_items.filter(quantity__lte=10),
                'items': inventory_items
            }
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch inventory data: {str(e)}")

    def _get_user_activity_data(self, date_from: str, date_to: str) -> dict:
        """Get user activity related data"""
        try:
            users = self.user_model.objects.filter(
                last_login__range=[date_from, date_to]
            )
            
            return {
                'total_users': users.count(),
                'active_users': users.filter(is_active=True).count(),
                'new_users': users.filter(date_joined__range=[date_from, date_to]).count(),
                'users': users
            }
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch user activity data: {str(e)}")
        
    def delete_report(self, report_id: str, user_id: str) -> bool:
        try:
            report = self.model.objects.get(
                id=report_id,
                generated_by_id=user_id
            )
            
            if report.file:
                report.file.delete(save=False)
                
            report.delete()
            return True
        except self.model.DoesNotExist:
            raise DatabaseException("Report not found or access denied")
        except Exception as e:
            raise DatabaseException(f"Failed to delete report: {str(e)}")