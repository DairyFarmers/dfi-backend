from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from users.models import UserRole
import logging
import os

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates default admin account if it doesn\'t exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # First ensure admin role exists
        self.stdout.write(self.style.NOTICE('Checking for admin role...'))
        try:
            admin_role = UserRole.objects.get(name='admin')
            self.stdout.write(self.style.SUCCESS('Found admin role'))
        except UserRole.DoesNotExist:
            self.stderr.write(
                self.style.ERROR('Admin role not found. Please run create_default_user_roles first.')
            )
            return

        # Check for existing admin user
        self.stdout.write(self.style.NOTICE('Checking for existing admin account...'))
        admin_exists = User.objects.filter(
            Q(is_superuser=True) | Q(role=admin_role)
        ).exists()

        if not admin_exists:
            try:
                email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@dfi.com')
                password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'Admin123!')
                
                admin = User.objects.create_superuser(
                    email=email,
                    password=password,
                    first_name='Admin',
                    last_name='User',
                    role=admin_role,
                    is_active=True
                )

                self.stdout.write('=' * 50)
                self.stdout.write(self.style.SUCCESS('Successfully created admin account'))
                self.stdout.write(self.style.NOTICE('Admin Account Details:'))
                self.stdout.write(f'Email: {email}')
                self.stdout.write(f'Password: {password}')
                self.stdout.write('=' * 50)
                self.stdout.write(
                    self.style.WARNING('Please change the default password after first login!')
                )
                
                logger.info('Created admin user account')
                
            except Exception as e:
                error_message = f'Failed to create admin account: {str(e)}'
                self.stderr.write(self.style.ERROR(error_message))
                logger.error(error_message)
        else:
            admin_users = User.objects.filter(Q(is_superuser=True) | Q(role=admin_role))
            
            self.stdout.write(self.style.WARNING('Admin account(s) already exist:'))
            self.stdout.write('=' * 50)
            for user in admin_users:
                self.stdout.write(
                    f"- {user.email} ({'Superuser' if user.is_superuser else 'Admin'})"
                )
            self.stdout.write('=' * 50)
            
            logger.info(f'Found {admin_users.count()} existing admin account(s)')