import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_role = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_roles')
    permissions = models.JSONField(default=dict)  # Store role-specific permissions
    priority = models.IntegerField(default=0)  # Higher number means higher priority

    class Meta:
        ordering = ['-priority', 'name']
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')

    def __str__(self):
        return self.name

    def get_all_permissions(self):
        """Get all permissions including inherited ones from parent roles"""
        all_permissions = self.permissions.copy()
        
        current_role = self
        while current_role.parent_role:
            parent_permissions = current_role.parent_role.permissions
            for key, value in parent_permissions.items():
                if key not in all_permissions:  # Child permissions override parent
                    all_permissions[key] = value
            current_role = current_role.parent_role
        
        return all_permissions

    def has_permission(self, permission_name):
        """Check if role has specific permission including inherited ones"""
        return self.get_all_permissions().get(permission_name, False)

    @classmethod
    def get_default_roles(cls):
        return [
            {
                "name": "admin",
                "description": "Administrator with full system access",
                "priority": 100,
                "permissions": {
                    # User Management
                    "can_manage_users": True,
                    "can_view_users": True,
                    "can_create_users": True,
                    "can_edit_users": True,
                    "can_delete_users": True,
                    "can_manage_roles": True,
                    
                    # System Management
                    "can_view_analytics": True,
                    "can_manage_system": True,
                    "can_view_logs": True,
                    "can_manage_settings": True,
                    
                    # Content Management
                    "can_manage_content": True,
                    "can_approve_content": True,
                    
                    # Financial Management
                    "can_view_financials": True,
                    "can_manage_financials": True,
                    
                    # API Access
                    "can_access_api": True,
                    "can_manage_api_keys": True
                }
            },
            {
                "name": "inventory_manager",
                "description": "Manages inventory and stock",
                "priority": 50,
                "permissions": {
                    # Inventory Management
                    "can_manage_inventory": True,
                    "can_view_stock": True,
                    "can_adjust_stock": True,
                    "can_manage_orders": True,
                    "can_view_orders": True,
                    "can_create_purchase_orders": True,
                    "can_approve_purchase_orders": True,
                    
                    # Stock Management
                    "can_manage_stock_levels": True,
                    "can_set_reorder_points": True,
                    "can_manage_suppliers": True,
                    
                    # Reports
                    "can_view_inventory_reports": True,
                    "can_export_inventory_data": True,
                    
                    # Basic Permissions
                    "can_access_api": True,
                    "can_view_users": True
                }
            },
            {
                "name": "sales_representative",
                "description": "Handles sales and customer relations",
                "priority": 40,
                "permissions": {
                    # Sales Management
                    "can_manage_sales": True,
                    "can_view_customers": True,
                    "can_create_orders": True,
                    "can_view_orders": True,
                    "can_manage_customers": True,
                    "can_view_product_pricing": True,
                    
                    # Customer Management
                    "can_create_customers": True,
                    "can_edit_customers": True,
                    "can_view_customer_history": True,
                    
                    # Order Management
                    "can_process_orders": True,
                    "can_apply_discounts": True,
                    "can_view_order_history": True,
                    
                    # Basic Permissions
                    "can_access_api": True,
                    "can_view_stock": True
                }
            },
            {
                "name": "farmer",
                "description": "Manages crops and farm operations",
                "priority": 30,
                "permissions": {
                    # Crop Management
                    "can_manage_crops": True,
                    "can_view_market_prices": True,
                    "can_manage_harvest": True,
                    "can_record_crop_data": True,
                    "can_view_crop_analytics": True,
                    
                    # Farm Operations
                    "can_manage_farm_inventory": True,
                    "can_record_farm_activities": True,
                    "can_manage_farm_workers": True,
                    
                    # Sales
                    "can_list_products": True,
                    "can_set_prices": True,
                    "can_view_orders": True,
                    
                    # Basic Permissions
                    "can_access_api": True,
                    "can_view_market_data": True
                }
            },
            {
                "name": "b2b",
                "description": "Business to Business operations",
                "priority": 35,
                "permissions": {
                    # B2B Operations
                    "can_view_wholesale": True,
                    "can_place_bulk_orders": True,
                    "can_view_market_analytics": True,
                    "can_access_bulk_pricing": True,
                    
                    # Order Management
                    "can_manage_b2b_orders": True,
                    "can_view_order_status": True,
                    "can_manage_subscriptions": True,
                    
                    # Analytics
                    "can_view_market_trends": True,
                    "can_export_reports": True,
                    
                    # Basic Permissions
                    "can_access_api": True,
                    "can_view_inventory": True
                }
            }
        ] 