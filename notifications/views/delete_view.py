from rest_framework.permissions import IsAuthenticated
from notifications.services.notification_service import NotificationService
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    service = NotificationService()
    
    def delete(self, request, id):
        try:
            logger.info(
                f"Attempting to delete notification with ID: {id}"
            )
            success = self.service.delete_notification(id)
            if success:
                logger.info(
                    f"Notification with ID {id} deleted successfully"
                )
                return Response({
                    'status': True,
                    'message': 'Notification deleted successfully'
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(
                    f"Notification with ID {id} not found"
                )
                return Response({
                    'status': False,
                    'message': 'Notification not found'
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Error deleting notification with ID {id}: {str(e)}"
            )
            return Response({
                'status': False,
                'message': 'An error occurred while deleting the notification',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)