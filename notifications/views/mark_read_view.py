from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from notifications.services.notification_service import NotificationService
from exceptions import DatabaseException, RepositoryException
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]
    notification_service = NotificationService()

    def get(self, request, pk):
        """Mark notifications as read"""
        try:
            result = self.notification_service.mark_notifications_as_read(
                user_id=request.user.id,
                notification_id=pk
            )

            return Response({
                "status": True,
                "message": "Notifications marked as read successfully",
                "data": result
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