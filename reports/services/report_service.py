from reports.models.report import Report
from django.utils.timezone import now
from users.models import UserActivityLog
from orders.models import Order
from inventories.models import Inventory

class ReportService:
    @staticmethod
    def generate_sales_report(user):
        orders = Order.objects.all().values("id", "product", "quantity", "total_price", "created_at")
        report = Report.objects.create(
            title="Sales Report",
            report_type="sales",
            generated_by=user,
            data=list(orders),
        )
        return report

    @staticmethod
    def generate_inventory_report(user):
        inventory = Inventory.objects.all().values("id", "name", "stock", "price")
        report = Report.objects.create(
            title="Inventory Report",
            report_type="inventory",
            generated_by=user,
            data=list(inventory),
        )
        return report

    @staticmethod
    def generate_user_activity_report(user):
        activity_logs = UserActivityLog.objects.all().values("user", "action", "timestamp", "ip_address")
        report = Report.objects.create(
            title="User Activity Report",
            report_type="user_activity",
            generated_by=user,
            data=list(activity_logs),
        )
        return report