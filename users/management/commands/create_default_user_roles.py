from django.core.management.base import BaseCommand
from users.models import UserRole
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates default user roles if they don\'t exist'

    def handle(self, *args, **kwargs):
        default_roles = [
            {
                'name': 'admin',
                'description': 'Administrator with full system access',
                'priority': 100,
                'permissions': {
                    # User Management
                    'can_manage_users': True,
                    'can_view_users': True,
                    'can_create_users': True,
                    'can_edit_users': True,
                    'can_delete_users': True,
                    'can_manage_roles': True,
                    
                    # System Management
                    'can_view_analytics': True,
                    'can_manage_system': True,
                    'can_view_logs': True,
                    'can_manage_settings': True,
                    
                    # All Module Access
                    'can_view_inventory': True,
                    'can_view_sales': True,
                    'can_view_orders': True,
                    'can_view_suppliers': True,
                    'can_view_reports': True,
                    
                    'can_manage_inventory': True,
                    'can_manage_sales': True,
                    'can_manage_orders': True,
                    'can_manage_suppliers': True,
                    'can_manage_reports': True,
                    'can_access_api': True
                }
            },
            {
                'name': 'inventory_manager',
                'description': 'Inventory manager with access to inventory data',
                'priority': 50,
                'permissions': {
                    # Inventory Management
                    'can_manage_inventory': True,
                    'can_view_stock': True,
                    'can_adjust_stock': True,
                    'can_manage_orders': True,
                    'can_view_orders': True,
                    'can_create_purchase_orders': True,
                    
                    # Supplier Management
                    'can_manage_suppliers': True,
                    'can_view_suppliers': True,
                    
                    # Reports
                    'can_view_inventory_reports': True,
                    'can_export_inventory_data': True,
                    
                    # Basic Access
                    'can_view_analytics': True,
                    'can_view_invetory': True,
                    'can_view_orders': True,
                    'can_view_sales': True,
                    'can_view_suppliers': True,
                    'can_view_reports': True,
                    'can_access_api': True,
                    'can_view_users': True
                }
            },
            {
                'name': 'sales_representative',
                'description': 'Sales representative with access to sales data',
                'priority': 40,
                'permissions': {
                    # Sales Management
                    'can_manage_sales': True,
                    'can_view_sales': True,
                    'can_create_sales': True,
                    'can_edit_sales': True,
                    
                    # Order Management
                    'can_view_orders': True,
                    'can_create_orders': True,
                    'can_edit_orders': True,
                    
                    # Customer Management
                    'can_manage_customers': True,
                    'can_view_customers': True,
                    
                    # Basic Access
                    'can_view_analytics': True,
                    'can_view_inventory': True,
                    'can_view_suppliers': True,
                    'can_view_orders': True,
                    'can_view_sales': True,
                    'can_access_api': True,
                    'can_view_inventory': True
                }
            },
            {
                'name': 'farmer',
                'description': 'Farmer with access to their own data',
                'priority': 30,
                'permissions': {
                    # Inventory Management
                    'can_view_inventory': True,
                    'can_view_stock': True,
                    
                    # Order Management
                    'can_view_orders': True,
                    'can_create_orders': True,
                    
                    # Profile Management
                    'can_edit_profile': True,
                    'can_view_profile': True,
                    
                    # Basic Access
                    'can_view_analytics': True,
                    'can_access_api': True
                }
            }
        ]

        for role_data in default_roles:
            role, created = UserRole.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'priority': role_data['priority'],
                    'permissions': role_data['permissions']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created {role_data['name']} role with {len(role_data['permissions'])} permissions")
                )
                logger.info(f"Created role: {role_data['name']}")
            else:
                # Update existing role with latest permissions
                role.description = role_data['description']
                role.priority = role_data['priority']
                role.permissions = role_data['permissions']
                role.save()
                
                self.stdout.write(
                    self.style.NOTICE(f"Updated {role_data['name']} role with {len(role_data['permissions'])} permissions")
                )
                logger.info(f"Updated role: {role_data['name']}")