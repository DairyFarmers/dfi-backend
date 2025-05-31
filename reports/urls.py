from django.urls import path
from reports.views import (
    ReportGenerateView,
    ReportListView,
    ReportDetailView,
    ReportDownloadView,
    ReportDeleteView
)

urlpatterns = [
    path('generate', ReportGenerateView.as_view(), name='report-generate'),
    path('list', ReportListView.as_view(), name='report-list'),
    path('<uuid:report_id>', ReportDetailView.as_view(), name='report-detail'),
    path('<uuid:report_id>/download', ReportDownloadView.as_view(), name='report-download'),
    path('<uuid:report_id>/delete', ReportDeleteView.as_view(), name='report-delete'),
]