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
        related_object_id: str = None,
        related_object_type: str = None
    ) -> Notification:
        """Create a new notification"""
        try:
            notification = Notification.objects.create(
                type=notification_type,
                title=title,
                message=message,
                user_id=user_id,
                related_object_id=related_object_id,
                related_object_type=related_object_type
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
    def get_notifications_by_user(user_id: int, mark_as_read: bool = False):
        """Get all notifications for a user"""
        try:
            notifications = Notification.objects.filter(user_id=user_id)
            
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
    def mark_as_read(user_id: int, notification_id: int) -> bool:
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