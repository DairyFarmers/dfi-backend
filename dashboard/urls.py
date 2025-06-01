# dashboard URL Configuration

from django.urls import path
from dashboard.views.dashboard_summary_view import DashboardSummaryView

urlpatterns = [
    path("summary", DashboardSummaryView.as_view(), name="dashboard-summary"),
]
