from django.db.models import Sum, Count, F, Q
from datetime import timedelta, date
from orders.models.order import Order
from inventories.models.inventory_item import InventoryItem
from users.models.user import User
from users.models.user_activity_log import UserActivityLog

class DashboardRepository:
    def get_total_orders():
        return Order.objects.count()

    def get_total_revenue():
        return Order.objects.aggregate(total_revenue=Sum("total_amount"))["total_revenue"] or 0

    def get_pending_orders():
        return Order.objects.filter(order_status="pending").count()

    def get_inventory_status():
        return InventoryItem.objects.aggregate(
            total_items=Count("id"),
            low_stock=Count("id", filter=Q(quantity__lt=10))
        )

    def get_user_statistics():
        return {
            "total_users": User.objects.count(),
            "admins": User.objects.filter(role="admin").count(),
            "inventory_managers": User.objects.filter(role="inventory_manager").count(),
            "shop_owners": User.objects.filter(role="shop_owner").count(),
            "farmers": User.objects.filter(role="farmer").count(),
        }

    def get_stock_summary():
        return InventoryItem.objects.aggregate(
            total_stock=Sum("quantity"),
            low_stock=Count("id", filter=Q(quantity__lt=10))
        )

    def get_orders_overview():
        return {
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(order_status="pending").count(),
            "completed_orders": Order.objects.filter(order_status="completed").count(),
        }

    def get_expiring_stock():
        return InventoryItem.objects.filter(expiry_date__lte=date.today() + timedelta(days=30))

    def get_sales_graph_data():
        sales_data = (
            Order.objects.extra({'order_date': "DATE(order_date)"})
            .values("order_date")
            .annotate(total_sales=Sum("total_amount"))
        )
        return sales_data