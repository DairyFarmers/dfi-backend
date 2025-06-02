from background_task import background
from django.utils import timezone
from datetime import timedelta
from inventories.models import InventoryItem
from django.db.models import Q
from notifications.models import Notification
from emails.services import EmailService
from notifications.tasks import send_email_notification, send_push_notification

class NotificationService:
    def __init__(self):
        self.email_service = EmailService()
        
    @staticmethod
    def send_email(subject, message, recipients):
        return send_email_notification.delay(subject, message, recipients)

    @staticmethod
    def send_push(user_id, message):
        return send_push_notification.delay(user_id, message)

    @background(schedule=60*60*24)  # Run daily
    def check_expiry_dates():
        """Check for products nearing expiry"""
        expiry_threshold = timezone.now() + timedelta(days=30)
        
        expiring_items = InventoryItem.objects.filter(
            Q(expiry_date__lte=expiry_threshold) & 
            Q(quantity__gt=0)
        )

        for item in expiring_items:
            days_until_expiry = (item.expiry_date - timezone.now().date()).days
            
            # Create notification
            NotificationService.create_expiry_notification(item.id, days_until_expiry)
            
            # Send email for items expiring within 7 days
            if days_until_expiry <= 7:
                NotificationService.send_expiry_email(item.id)

    @staticmethod
    def create_expiry_notification(item_id: str, days: int):
        """Create notification for expiring product"""
        item = InventoryItem.objects.get(id=item_id)
        notification = Notification.objects.create(
            type='expiry',
            title=f'Product Expiring Soon: {item.name}',
            message=f'Product will expire in {days} days',
            user=item.supplier.account_manager,
            related_object_id=item.id,
            related_object_type='inventory_item'
        )
        return notification

    @staticmethod
    def send_expiry_email(item_id: str):
        """Send email for expiring product"""
        item = InventoryItem.objects.get(id=item_id)
        context = {
            'item_name': item.name,
            'expiry_date': item.expiry_date,
            'quantity': item.quantity,
            'storage_condition': item.storage_condition,
        }
        
        email_service = EmailService()
        return email_service.send_notification_email(
            to_email=item.supplier.account_manager.email,
            subject=f'Urgent: Product Expiring Soon - {item.name}',
            template_name='emails/product_expiry.html',
            context=context
        )