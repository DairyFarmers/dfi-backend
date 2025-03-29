from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from users.models.user_activity_log import UserActivityLog
from users.serializers.user_activity_logs_serializer import UserActivityLogsSerializer

class UserActivityLogsView(APIView):
    @swagger_auto_schema(responses={200: UserActivityLogsSerializer(many=True)})
    def get(self, request):
        logs = UserActivityLog.objects.all().order_by("-timestamp")[:100]
        print(logs)
        serializer = UserActivityLogsSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
