from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reports.models.report import Report
from django.http import FileResponse
from django.utils.timezone import now
import os
from utils import setup_logger

logger = setup_logger(__name__)

class ReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, report_id):
        try:
            logger.info(f"{request.user} is downloading report {report_id}")
            report = Report.objects.get(id=report_id, generated_by=request.user)
            
            if not report.file:
                return Response(
                    {"message": "Report file not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            if report.status != 'completed':
                return Response(
                    {"message": "Report is not ready yet"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_path = report.file.path
            if not os.path.exists(file_path):
                return Response(
                    {"message": "Report file not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            content_types = {
                'pdf': 'application/pdf',
                'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'csv': 'text/csv'
            }

            timestamp = now().strftime('%Y%m%d_%H%M%S')
            filename = f"{report.report_type}_report_{timestamp}.{report.format}"

            response = FileResponse(
                open(file_path, 'rb'),
                content_type=content_types.get(report.format, 'application/octet-stream')
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Report.DoesNotExist:
            logger.error(f"Report {report_id} not found for user {request.user}")
            return Response(
                {"error": "Report not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error downloading report {report_id}: {e}")
            return Response(
                {"error": "Failed to download report"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )