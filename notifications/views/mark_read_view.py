from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from notifications.services.notification_service import NotificationService
from exceptions import DatabaseException, RepositoryException
from notifications.serializers import NotificationSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]
    notification_service = NotificationService()

    def get(self, request, id):
        """Mark notifications as read"""
        try:
            result = self.notification_service.mark_notifications_as_read(
                user_id=request.user.id,
                notification_id=id
            )
            notification = self.notification_service.get_notification_by_id(id)
            if not notification:
                return Response({
                    "status": False,
                    "message": "Notification not found"
                }, status=status.HTTP_404_NOT_FOUND)
                
            serializer = NotificationSerializer(notification)
            return Response({
                "status": True,
                "message": "Notifications marked as read successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except (DatabaseException, RepositoryException) as e:
            logger.error(f"Failed to mark notifications as read: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            logger.error(f"Unexpected error marking notifications as read: {str(e)}")
            return Response({
                "status": False,
                "message": "An unexpected error occurred"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)