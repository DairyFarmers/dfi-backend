from celery import shared_task
from django.utils import timezone
from .models import Notification
from datetime import timedelta
from django.db.models import Q
from inventories.models import InventoryItem
from notifications.services import NotificationService
from django.contrib.auth import get_user_model
from notifications.services import EmailService
from utils import setup_logger

logger = setup_logger(__name__)

@shared_task
def check_inventory_expiry():
    """Check inventory items for expiry and create notifications"""
    notification_service = NotificationService()
    expiry_threshold = timezone.now().date() + timedelta(days=30)
    
    # Get items expiring in next 30 days
    expiring_items = InventoryItem.objects.filter(
        Q(expiry_date__lte=expiry_threshold) & 
        Q(quantity__gt=0)
    ).select_related('supplier')

    logger.info(f"Found {expiring_items.count()} items expiring within 30 days")

    for item in expiring_items:
        days_until_expiry = (item.expiry_date - timezone.now().date()).days
        priority = 'high' if days_until_expiry <= 7 else 'medium'
        
        # Get users to notify based on roles
        inventory_managers = get_user_model().objects.filter(
            role__name='inventory_manager'
        )
        admins = get_user_model().objects.filter(
            role__name='admin'
        )
        
        for user in inventory_managers:
            notification = notification_service.create_notification(
                notification_type='expiry',
                title=f'Inventory Alert: Product Expiring Soon',
                message=(f'Product {item.name} (Batch: {item.batch_number}) '
                        f'will expire in {days_until_expiry} days. '
                        f'Current quantity: {item.quantity}. '
                        f'Please take necessary action.'),
                user_id=user.id,
                priority=priority,
                related_object_id=str(item.id),
                related_object_type='inventory_item'
            )
            send_notification_email.delay(notification.id)
            
        for user in admins:
            notification = notification_service.create_notification(
                notification_type='expiry',
                title=f'Admin Alert: Expiring Inventory',
                message=(f'Product {item.name} from supplier {item.supplier.name} '
                        f'will expire in {days_until_expiry} days. '
                        f'Quantity: {item.quantity}. '
                        f'Please review inventory management.'),
                user_id=user.id,
                priority=priority,
                related_object_id=str(item.id),
                related_object_type='inventory_item'
            )
            send_notification_email.delay(notification.id)
        
        logger.info(f"Created expiry notification for item {item.name}")
        
    return f"Processed {expiring_items.count()} expiring items"

@shared_task
def process_notification_queue():
    """Process pending notifications and send emails"""
    notifications = Notification.objects.filter(
        sent_email=False,
        created_at__gte=timezone.now() - timezone.timedelta(days=1)
    )
    print('Processing notifications:', notifications.count())
    
    for notification in notifications:
        try:
            send_notification_email.delay(notification.id)
        except Exception as e:
            logger.error(f"Failed to queue email for notification {notification.id}: {str(e)}")

@shared_task
def send_notification_email(notification_id):
    """Send email for a specific notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        full_name = f"{notification.user.first_name} \
            {notification.user.last_name}".strip()
        service = EmailService()
        email_sent = service.send_product_expiry_email(
            notification.user.email, 
            full_name,
            notification.priority,
            notification.notification_title,
            notification.message,
        )
        
        if email_sent:
            logger.info(f"Email sent for notification \
                {notification_id} to {notification.user.email}")
            notification.sent_email = True
            notification.save(update_fields=['sent_email', 'updated_at'])
        else:
            logger.error(f"Failed to send email for notification \
                {notification_id}")
        
        logger.info(f"Email sent for notification \
            {notification_id} to {notification.user.email}")
        notification.sent_email = True
        notification.save(update_fields=['sent_email', 'updated_at'])
    except Exception as e:
        logger.error(
            f"Error in send_notification_email for \
                {notification_id}: {str(e)}"
            )