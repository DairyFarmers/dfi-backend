from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sales.views.sale_view import SaleViewSet
from sales.views.payment_view import PaymentViewSet

router = DefaultRouter()
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]