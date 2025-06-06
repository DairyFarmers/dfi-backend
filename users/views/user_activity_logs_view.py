from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from users.models.user_activity_log import UserActivityLog
from users.serializers.user_activity_logs_serializer import UserActivityLogsSerializer
from rest_framework.pagination import PageNumberPagination

class UserActivityLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100

class UserActivityLogsView(APIView):
    pagination_class = UserActivityLogPagination

    @swagger_auto_schema(responses={200: UserActivityLogsSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)

        try:
            size = int(size)
            if size < 1 or size > 100:
                return Response({'detail': 'Invalid size parameter'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'Invalid size parameter'}, status=status.HTTP_400_BAD_REQUEST)

        logs = UserActivityLog.objects.all().order_by("-timestamp")
        paginator = self.pagination_class()
        paginated_logs = paginator.paginate_queryset(logs, request)
        serializer = UserActivityLogsSerializer(paginated_logs, many=True)
        return paginator.get_paginated_response(serializer.data)