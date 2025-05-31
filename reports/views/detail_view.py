from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.models.report import Report
from reports.serializers.report_serializer import ReportSerializer

class ReportDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReportSerializer()})
    def get(self, request, report_id):
        try:
            report = Report.objects.get(id=report_id, generated_by=request.user)
            serializer = ReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Report.DoesNotExist:
            return Response(
                {"message": "Report not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

