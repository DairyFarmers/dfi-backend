from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reports.models.report import Report
from django.http import FileResponse
import os

class ReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, report_id):
        try:
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

            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response

        except Report.DoesNotExist:
            return Response(
                {"message": "Report not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Failed to download report", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )