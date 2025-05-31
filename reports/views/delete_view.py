from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.services.report_service import ReportService

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
            ReportService.delete_report(report_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except ValueError as e:
            return Response(
                {"message": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "message": "Failed to delete report",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )