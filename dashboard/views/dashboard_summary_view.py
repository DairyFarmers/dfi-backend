from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.repositories.dashboard_repository import DashboardRepository

class DashboardSummaryView(APIView):
    repository = DashboardRepository
    service = DashboardService(repository)

    @swagger_auto_schema(
        responses={200: "Returns dashboard summary"}
    )
    def get(self, request):
        data = self.service.get_dashboard_summary()
        return Response(data, status=status.HTTP_200_OK)