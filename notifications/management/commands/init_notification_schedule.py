from django.core.management.base import BaseCommand
from notifications.services.notification_service import NotificationService

class Command(BaseCommand):
    help = 'Initialize notification schedules'

    def handle(self, *args, **options):
        service = NotificationService()
        service.schedule_expiry_checks()
        self.stdout.write(
            self.style.SUCCESS('Successfully initialized notification schedules')
        )