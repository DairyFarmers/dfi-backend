# dashboard URL Configuration

from django.contrib import admin
from django.urls import path
from dashboard.views.dashboard_summary_view import DashboardSummaryView
from dashboard.views.stock_summary_view import StockSummaryView
from dashboard.views.orders_overview_view import OrdersOverviewView
from dashboard.views.expiring_stock_view import ExpiringStockView
from dashboard.views.sales_graph_view import SalesGraphView

urlpatterns = [
    path("summary", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("stock-summary", StockSummaryView.as_view(), name="stock-summary"),
    path("orders-overview", OrdersOverviewView.as_view(), name="orders-overview"),
    path("expiring-stock", ExpiringStockView.as_view(), name="expiring-stock"),
    path("sales-graph", SalesGraphView.as_view(), name="sales-graph"),
]
