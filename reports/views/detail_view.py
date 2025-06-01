from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.models.report import Report
from reports.serializers.report_serializer import ReportSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class ReportDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReportSerializer()})
    def get(self, request, report_id):
        try:
            logger.info(f"{request.user} is retrieving report {report_id}")
            report = Report.objects.get(id=report_id, generated_by=request.user)
            serializer = ReportSerializer(report)
            return Response({
                "status": True,
                "message": "Report retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Report.DoesNotExist:
            logger.error(f"Report {report_id} not found for user {request.user}")
            return Response(
                {"message": "Report not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving report {report_id}: {e}")
            return Response(
                {"message": "Failed to retrieve report"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

