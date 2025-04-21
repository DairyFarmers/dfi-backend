from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from reports.models.report import Report
from reports.serializers.report_serializer import ReportSerializer
from reports.services.report_service import ReportService

class ReportGenerateView(APIView):
    @swagger_auto_schema(request_body=None, responses={201: "Report Generated"})
    def post(self, request, report_type):
        user = request.user

        if report_type == "sales":
            report = ReportService.generate_sales_report(user)
        elif report_type == "inventory":
            report = ReportService.generate_inventory_report(user)
        elif report_type == "user_activity":
            report = ReportService.generate_user_activity_report(user)
        else:
            return Response({"message": "Invalid report type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)

class ReportListView(APIView):
    @swagger_auto_schema(responses={200: ReportSerializer(many=True)})
    def get(self, request):
        reports = Report.objects.all().order_by("-generated_at")
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportDetailView(APIView):
    @swagger_auto_schema(responses={200: ReportSerializer()})
    def get(self, request, report_id):
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
