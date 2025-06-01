from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.models.report import Report
from reports.serializers.report_serializer import ReportSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class ReportListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReportSerializer(many=True)})
    def get(self, request):
        try:
            logger.info(f"{request.user} is retrieving their reports")
            reports = Report.objects.filter(
                generated_by=request.user
            ).select_related('generated_by')
            serializer = ReportSerializer(
                reports, 
                many=True,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving reports: {e}")
            return Response(
                {"error": "Failed to retrieve reports"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
