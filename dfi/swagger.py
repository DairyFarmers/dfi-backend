from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Dairy Inventory Management API",
        default_version='v1',
        description="""
        REST API Documentation for Dairy Inventory Management System.
        
        The API provides endpoints for:
        * Inventory Management
        * Supplier Management
        * Order Processing
        * Temperature Monitoring
        * Stock Alerts
        * User Management
        """,
        terms_of_service="",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=f"{'https' if settings.SECURE_COOKIE else 'http'}://{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000'}",
)
