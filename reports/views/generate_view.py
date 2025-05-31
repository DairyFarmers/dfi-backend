from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.serializers import ReportSerializer, ReportGenerateSerializer
from reports.services.report_service import ReportService
from django.http import HttpResponse

class ReportGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReportGenerateSerializer,
        responses={201: ReportSerializer()}
    )
    def post(self, request):
        serializer = ReportGenerateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            report = ReportService.generate_report(
                user=request.user,
                **serializer.validated_data
            )
            
            if serializer.validated_data['format'] == 'pdf':
                response = HttpResponse(
                    content=report.file, 
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = f'attachment; filename="{report.file.name}"'
                return response
            elif serializer.validated_data['format'] in ['excel', 'csv']:
                content_types = {
                    'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'csv': 'text/csv'
                }
                response = HttpResponse(
                    content=report.file,
                    content_type=content_types[serializer.validated_data['format']]
                )
                response['Content-Disposition'] = f'attachment; filename="{report.file.name}"'
                return response
            
            # Default JSON response for report metadata
            return Response(
                ReportSerializer(report).data, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Error generating report:", str(e))
            return Response(
                {
                    "message": "Failed to generate report", 
                    "error": str(e)
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )