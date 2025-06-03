from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from notifications.services.notification_service import NotificationService
from notifications.serializers import NotificationSerializer
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    notification_service = NotificationService()

    def get(self, request):
        """Get notifications for the current user"""
        try:
            fetch_all = request.query_params.get('all', 'false').lower() == 'true'
            notifications = self.notification_service.get_user_notifications(
                user_id=request.user.id,
            )
            serializer = NotificationSerializer(notifications['notifications'], many=True)

            if fetch_all:
                return Response({
                    "status": True,
                    "message": "All notifications fetched successfully",
                    "data": {
                        "notifications": {
                            'results': serializer.data,
                            'count': len(serializer.data),
                        },
                        "stats": {
                            'total_count': notifications['total_count'],
                            'unread_count': notifications['unread_count']
                        }
                    }
                }, status=status.HTTP_200_OK)
            
            try:
                page = int(request.query_params.get('page', 1))
                page_size = int(request.query_params.get('size', 10))
            except ValueError:
                page = 1
                page_size = 10
                
            paginator = Paginator(serializer.data, page_size)
            current_page = paginator.get_page(page)
            return Response({
                "status": True,
                "message": "Notifications fetched successfully",
                "data": {
                        'notifications': {
                            'results': current_page.object_list,
                            'count': paginator.count,
                            'num_pages': paginator.num_pages,
                            'next': page + 1 if current_page.has_next() else None,
                            'previous': page - 1 if current_page.has_previous() else None
                        },
                        "stats": {
                            'total_count': notifications['total_count'],
                            'unread_count': notifications['unread_count']
                        }
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error fetching notifications: {str(e)}")
            return Response({
                "status": False,
                "message": "An unexpected error occurred"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)