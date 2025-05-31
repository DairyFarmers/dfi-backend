from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sets up initial user roles and admin account'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE('Setting up user roles...'))
            call_command('create_default_user_roles')
            
            self.stdout.write(self.style.NOTICE('Creating admin account...'))
            call_command('create_default_admin')
            
            self.stdout.write(self.style.SUCCESS('Initial setup completed successfully'))
            
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Setup failed: {str(e)}')
            )
            logger.error(f'Setup failed: {str(e)}')