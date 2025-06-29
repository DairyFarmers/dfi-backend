"""dfi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/inventory/', include('inventories.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('chats.urls')),
    path('api/v1/suppliers/', include('suppliers.urls')),
    path('api/v1/', include('sales.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/search/', include('search.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), 
            name='schema-json'
        ),
        path(
            'swagger/', 
            schema_view.with_ui('swagger', cache_timeout=0), 
            name='schema-swagger-ui'
        ),
        path(
            'redoc/', 
            schema_view.with_ui('redoc', cache_timeout=0), 
            name='schema-redoc'
        ),
    ]
