from django.db import DatabaseError
from notifications.models import Notification
from exceptions import DatabaseException, RepositoryException
from django.utils import timezone
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationRepository:
    @staticmethod
    def create_notification(
        notification_type: str,
        title: str,
        message: str,
        user_id: int,
        **kwargs: dict
    ) -> Notification:
        """Create a new notification"""
        try:
            notification = Notification.objects.create(
                notification_type=notification_type,
                notification_title=title,
                message=message,
                user_id=user_id,
                priority=kwargs.get('priority', 'medium'),
                related_object_id=kwargs.get('related_object_id'),
                related_object_type=kwargs.get('related_object_type')
            )
            logger.info(
                f"Created notification: {notification.id} for user: {user_id}"
            )
            return notification
        except DatabaseError as e:
            logger.error(f"Database error creating notification: {str(e)}")
            raise DatabaseException("Failed to create notification")
        except Exception as e:
            logger.error(f"Repository error creating notification: {str(e)}")
            raise RepositoryException("Failed to create notification")

    @staticmethod
    def get_notifications_by_user(user_id, mark_as_read: bool = False):
        """Get all notifications for a user"""
        try:
            notifications = Notification.objects.filter(
                user_id=user_id
            )
            
            if mark_as_read:
                notifications.filter(read=False).update(
                    read=True,
                    read_at=timezone.now()
                )

            return notifications
        except DatabaseError as e:
            logger.error(f"Database error fetching notifications: {str(e)}")
            raise DatabaseException("Failed to fetch notifications")
        except Exception as e:
            logger.error(f"Repository error fetching notifications: {str(e)}")
            raise RepositoryException("Failed to fetch notifications")

    @staticmethod
    def get_notification_by_id(notification_id):
        """Get a notification by its ID"""
        try:
            notification = Notification.objects.get(
                id=notification_id
            )
            return notification
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} does not exist")
            return None
        except DatabaseError as e:
            logger.error(f"Database error fetching notification: {str(e)}")
            raise DatabaseException("Failed to fetch notification by ID")
        except Exception as e:
            logger.error(f"Repository error fetching notification: {str(e)}")
            raise RepositoryException("Failed to fetch notification by ID")

    @staticmethod
    def mark_as_read(user_id, notification_id) -> bool:
        """Mark a notification as read"""
        try:
            now = timezone.now()
            result = Notification.objects.filter(
                id=notification_id, 
                user_id=user_id,
                read=False
            ).update(
                read=True,
                read_at=now,
                updated_at=now
            )
            
            if result:
                logger.info(f"Marked notification {notification_id} as read")
            
            return bool(result)
        except DatabaseError as e:
            logger.error(f"Database error marking notification as read: {str(e)}")
            raise DatabaseException("Failed to mark notification as read")
        except Exception as e:
            logger.error(f"Repository error marking notification as read: {str(e)}")
            raise RepositoryException("Failed to mark notification as read")
    
    @staticmethod
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        try:
            now = timezone.now()
            result = Notification.objects.filter(
                user_id=user_id,
                read=False
            ).update(
                read=True,
                read_at=now,
                updated_at=now
            )
            
            logger.info(f"Marked {result} notifications as read for user {user_id}")
            return result
        except DatabaseError as e:
            logger.error(f"Database error marking all notifications as read: {str(e)}")
            raise DatabaseException("Failed to mark all notifications as read")
        except Exception as e:
            logger.error(f"Repository error marking all notifications as read: {str(e)}")
            raise RepositoryException("Failed to mark all notifications as read")
    
    def delete_notification(self, notification_id) -> bool:
        """Delete a notification by its ID"""
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            logger.info(f"Deleted notification with ID {notification_id}")
            return True
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} does not exist")
            return False
        except DatabaseError as e:
            logger.error(f"Database error deleting notification: {str(e)}")
            raise DatabaseException("Failed to delete notification")
        except Exception as e:
            logger.error(f"Repository error deleting notification: {str(e)}")
            raise RepositoryException("Failed to delete notification")
        
    def delete_old_notifications(self, days: int = 30):
        """Delete notifications older than specified days"""
        try:
            threshold_date = timezone.now() - timezone.timedelta(days=days)
            return Notification.objects.filter(
                created_at__lt=threshold_date,
                read=True
            ).delete()
        except Exception as e:
            logger.error(f"Repository error deleting old notifications: {str(e)}")
            raise RepositoryException("Failed to delete old notifications")
        
    def get_pending_email_notifications(self):
        """Get notifications that haven't been emailed yet"""
        try:
            return Notification.objects.filter(
                sent_email=False
            ).select_related('user')
        except Exception as e:
            logger.error(f"Repository error fetching pending email notifications: {str(e)}")
            raise RepositoryException("Failed to fetch pending email notifications")

    def mark_email_sent(self, notification_id: int):
        """Mark notification as emailed"""
        try:
            return Notification.objects.filter(
                id=notification_id
            ).update(
                sent_email=True,
                updated_at=timezone.now()
            )
        except Exception as e:
            logger.error(f"Repository error marking email as sent: {str(e)}")
            raise RepositoryException("Failed to mark email as sent")