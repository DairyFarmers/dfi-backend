from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from reports.models.report import Report
from reports.serializers.report_serializer import ReportSerializer

class ReportListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ReportSerializer(many=True)})
    def get(self, request):
        reports = Report.objects.filter(
            generated_by=request.user
        ).select_related('generated_by')
        serializer = ReportSerializer(
            reports, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
