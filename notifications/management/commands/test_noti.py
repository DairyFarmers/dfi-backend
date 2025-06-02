from django.core.management.base import BaseCommand
from notifications.tasks import check_product_expiry
from inventories.models import InventoryItem
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Test notification system by creating test data and running checks'

    def handle(self, *args, **options):
        # Create test inventory item with near expiry date
        test_item = InventoryItem.objects.create(
            name='Test Product',
            quantity=10,
            expiry_date=timezone.now().date() + timedelta(days=5),
            # Add other required fields
        )

        self.stdout.write('Created test inventory item')

        # Run expiry check
        check_product_expiry()

        self.stdout.write(self.style.SUCCESS('Notification test completed'))