from django.http import JsonResponse
from rest_framework import status
from django.urls import resolve
from django.conf import settings

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define permission requirements for specific URL patterns
        self.permission_map = {
            # User Management
            'user-list': ['can_view_users'],
            'user-detail': ['can_view_users'],
            'registration': ['can_create_users'],
            
            # Role Management
            'role-list': ['can_manage_roles'],
            'role-detail': ['can_manage_roles'],
            'initialize-roles': ['can_manage_roles'],
            
            # Inventory Management
            'inventory-list': ['can_view_stock'],
            'inventory-detail': ['can_view_stock'],
            'inventory-create': ['can_manage_inventory'],
            'inventory-update': ['can_manage_inventory'],
            'inventory-delete': ['can_manage_inventory'],
            
            # Order Management
            'order-list': ['can_view_orders'],
            'order-detail': ['can_view_orders'],
            'order-create': ['can_create_orders'],
            'order-update': ['can_process_orders'],
            
            # Customer Management
            'customer-list': ['can_view_customers'],
            'customer-detail': ['can_view_customers'],
            'customer-create': ['can_create_customers'],
            'customer-update': ['can_edit_customers'],
            
            # Farm Management
            'crop-list': ['can_manage_crops'],
            'crop-detail': ['can_manage_crops'],
            'harvest-manage': ['can_manage_harvest'],
            
            # B2B Operations
            'wholesale-view': ['can_view_wholesale'],
            'bulk-order': ['can_place_bulk_orders'],
            'market-analytics': ['can_view_market_analytics']
        }

    def __call__(self, request):
        # Skip middleware if user is not authenticated
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return self.get_response(request)

        # Get current URL pattern name
        try:
            url_name = resolve(request.path_info).url_name
        except:
            url_name = None

        # Skip permission check if URL is not in permission map
        if not url_name or url_name not in self.permission_map:
            return self.get_response(request)

        # Get required permissions for this URL
        required_permissions = self.permission_map[url_name]

        # Check if user has all required permissions
        has_permission = all(
            request.user.has_permission(perm) 
            for perm in required_permissions
        )

        if not has_permission:
            return JsonResponse({
                'error': 'Permission denied',
                'detail': f'Required permissions: {", ".join(required_permissions)}'
            }, status=status.HTTP_403_FORBIDDEN)

        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Additional processing for class-based views with custom permissions"""
        if hasattr(view_func, 'view_class'):
            view_class = view_func.view_class
            
            # Check for custom permission requirements in the view
            if hasattr(view_class, 'required_permissions'):
                if not request.user.is_authenticated:
                    return JsonResponse({
                        'error': 'Authentication required'
                    }, status=status.HTTP_401_UNAUTHORIZED)

                required_permissions = view_class.required_permissions
                has_permission = all(
                    request.user.has_permission(perm) 
                    for perm in required_permissions
                )

                if not has_permission:
                    return JsonResponse({
                        'error': 'Permission denied',
                        'detail': f'Required permissions: {", ".join(required_permissions)}'
                    }, status=status.HTTP_403_FORBIDDEN)

        return None 