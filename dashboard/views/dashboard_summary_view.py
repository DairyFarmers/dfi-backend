from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.repositories.dashboard_repository import DashboardRepository

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    repository = DashboardRepository
    service = DashboardService(repository)

    @swagger_auto_schema(
        responses={200: "Returns dashboard summary"}
    )
    def get(self, request):
        role = request.user.role

        if role == "admin":
            data = {
                "user_statistics": self.service.get_user_statistics(),
                "stock_summary": self.service.get_stock_summary(),
                "orders_overview": self.service.get_orders_overview(),
            }
        return Response(data, status=status.HTTP_200_OK)