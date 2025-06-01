from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.services.report_service import ReportService
from utils import setup_logger

logger = setup_logger(__name__)

class ReportDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete a report",
        responses={
            204: "Report deleted successfully",
            404: "Report not found",
            403: "Permission denied"
        }
    )
    def delete(self, request, report_id):
        try:
            logger.info(f"{request.user} is attempting to delete report {report_id}")
            ReportService.delete_report(report_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            logger.error(f"Error deleting report {report_id}: {e}")
            return Response(
                {"message": "Report not found or invalid ID"},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionError as e:
            logger.error(f"Permission denied for user {request.user} on report {report_id}: {e}")
            return Response(
                {"message": "You do not have permission to delete this report"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            logger.error(f"Unexpected error deleting report {report_id}: {e}")
            return Response(
                {"message": "Failed to delete report"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )