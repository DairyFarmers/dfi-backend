from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from inventories.models import InventoryItem
from notifications.repositories.notification_repository import NotificationRepository
from emails.services import EmailService
from exceptions import RepositoryException
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationService:
    def __init__(self):
        self.email_service = EmailService()
        self.notification_repository = NotificationRepository()

    def get_user_notifications(self, user_id: int):
        """Get all notifications for a user"""
        try:
            notifications = self.notification_repository.get_notifications_by_user(user_id)
            return {
                "notifications": notifications,
                "total_count": notifications.count(),
                "unread_count": notifications.filter(read=False).count()
            }
        except Exception as e:
            logger.error(f"Failed to get notifications for user {user_id}: {str(e)}")
            raise RepositoryException("Failed to fetch notifications")

    def mark_notifications_as_read(self, user_id: int, notification_id: int):
        """Mark specific notifications as read"""
        try:
            updated_count = self.notification_repository.mark_as_read(
                user_id=user_id,
                notification_id=notification_id
            )
            logger.info(f"Marked {updated_count} notifications as read for user {user_id}")
            return {
                "updated_count": updated_count,
                "notification_ids": notification_id
            }
        except Exception as e:
            logger.error(f"Failed to mark notifications as read: {str(e)}")
            raise RepositoryException("Failed to mark notifications as read")

    def mark_all_as_read(self, user_id: int):
        """Mark all notifications as read for a user"""
        try:
            updated_count = self.notification_repository.mark_all_as_read(user_id)
            logger.info(f"Marked all notifications as read for user {user_id}")
            return {
                "updated_count": updated_count
            }
        except Exception as e:
            logger.error(f"Failed to mark all notifications as read: {str(e)}")
            raise RepositoryException("Failed to mark all notifications as read")
        
    def create_notification(self, notification_type: str, title: str, 
                          message: str, user_id: int, **kwargs):
        """Create a new notification"""
        try:
            notification = self.notification_repository.create_notification(
                notification_type=notification_type,
                title=title,
                message=message,
                user_id=user_id,
                **kwargs
            )
            logger.info(f"Created notification {notification.id} for user {user_id}")
            return notification
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")
            raise RepositoryException("Failed to create notification")

    def check_inventory_expiry(self):
        """Check for products nearing expiry and send notifications"""
        try:
            expiry_threshold = timezone.now() + timedelta(days=30)
            expiring_items = InventoryItem.objects.filter(
                Q(expiry_date__lte=expiry_threshold) & 
                Q(quantity__gt=0)
            )

            for item in expiring_items:
                try:
                    days_until_expiry = (item.expiry_date - timezone.now().date()).days
                    
                    # Create notification
                    self._create_expiry_notification(item, days_until_expiry)
                    
                    # Send email for critical expiry (7 days)
                    if days_until_expiry <= 7:
                        self._send_expiry_email(item)

                except Exception as e:
                    logger.error(f"Failed to process expiry for item {item.id}: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Failed to check expiry dates: {str(e)}")
            raise RepositoryException("Failed to check inventory expiry")

    def _create_expiry_notification(self, item: InventoryItem, days: int):
        """Create notification for expiring product"""
        return self.create_notification(
            notification_type='expiry',
            title=f'Product Expiring Soon: {item.name}',
            message=f'Product will expire in {days} days',
            user_id=item.supplier.account_manager.id,
            related_object_id=item.id,
            related_object_type='inventory_item'
        )

    def _send_expiry_email(self, item: InventoryItem):
        """Send email for expiring product"""
        try:
            context = {
                'item_name': item.name,
                'expiry_date': item.expiry_date,
                'quantity': item.quantity,
                'storage_condition': item.storage_condition,
            }
            
            self.email_service.send_notification_email(
                to_email=item.supplier.account_manager.email,
                subject=f'Urgent: Product Expiring Soon - {item.name}',
                template_name='emails/product_expiry.html',
                context=context
            )
            logger.info(f"Sent expiry email for item {item.id}")

        except Exception as e:
            logger.error(f"Failed to send expiry email for item {item.id}: {str(e)}")
            raise RepositoryException("Failed to send expiry email")