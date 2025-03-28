# orders URL Configuration

from django.contrib import admin
from django.urls import path
from orders.views.order_list_view import OrderListView
from orders.views.order_detail_view import OrderDetailView
from orders.views.order_add_view import OrderAddView

urlpatterns = [
    path("list", OrderListView.as_view(), name="order-list"),
    path("item/<int:order_id>", OrderDetailView.as_view(), name="order-detail"),
    path("add", OrderAddView.as_view(), name="order-add"),
]
