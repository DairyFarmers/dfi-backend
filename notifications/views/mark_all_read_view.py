from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from notifications.services.notification_service import NotificationService
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationMarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]
    notification_service = NotificationService()

    def get(self, request):
        """Mark all notifications as read for the current user"""
        try:
            result = self.notification_service.mark_all_as_read(
                user_id=request.user.id
            )

            return Response({
                "status": True,
                "message": "All notifications marked as read successfully",
                "data": {
                    "updated_count": result["updated_count"]
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error marking all notifications as read: {str(e)}")
            return Response({
                "status": False,
                "message": "An unexpected error occurred"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)