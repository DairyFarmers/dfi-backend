from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        fetch_all = request.query_params.get('fetch_all', 'false').lower() == 'true'

        if fetch_all:
            serializer = NotificationSerializer(notifications, many=True)
            return Response({
                "status": True,
                "message": "All notifications fetched successfully",
                "data": {
                    "results": serializer.data,
                    "count": notifications.count()
                }
            }, status=status.HTTP_200_OK)

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('size', 10)
        paginator = Paginator(notifications, page_size)
        current_page = paginator.get_page(page)
        serializer = NotificationSerializer(current_page, many=True)
        
        mock_data = [
            {
                "id": 1,
                "title": "Welcome to the platform!",
                "message": "Thank you for joining us. We hope you have a great experience.",
                "read": False,
                "created_at": "2023-10-01T12:00:00Z",
                "type": "Welcome"
            },
            {
                "id": 2,
                "title": "New feature available",
                "message": "Check out our new feature that allows you to customize your profile.",
                "read": True,
                "created_at": "2023-10-02T14:30:00Z",
                "type": "Feature Update"
            }
        ]
        return Response({
            "status": True,
            "message": "Notifications fetched successfully",
            "data": {
                "results": mock_data,
                "count": 2
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        notification_ids = request.data.get('notification_ids', [])
        Notification.objects.filter(
            id__in=notification_ids,
            user=request.user
        ).update(read=True)
        
        return Response(status=status.HTTP_200_OK)