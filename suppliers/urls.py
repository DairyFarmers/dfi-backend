from django.urls import path
from suppliers.views import (
    SupplierListView,
    SupplierDetailView
)

app_name = 'suppliers'

urlpatterns = [
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('<int:pk>', SupplierDetailView.as_view(), name='supplier-detail'),
] 