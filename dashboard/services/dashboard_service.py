class DashboardService:
    def __init__(self, repository):
        self.repository = repository

    def get_dashboard_summary(self):
        return {
            "total_orders": self.repository.get_total_orders(),
            "total_revenue": self.repository.get_total_revenue(),
            "pending_orders": self.repository.get_pending_orders(),
            "inventory_status": self.repository.get_inventory_status(),
            "user_statistics": self.repository.get_user_statistics(),
        }
    
    def get_user_statistics(self):
        return self.repository.get_user_statistics()

    def get_stock_summary(self):
        return self.repository.get_stock_summary()

    def get_orders_overview(self):
        return self.repository.get_orders_overview()

    def get_expiring_stock(self):
        return self.repository.get_expiring_stock()

    def get_sales_graph_data(self):
        return self.repository.get_sales_graph_data()