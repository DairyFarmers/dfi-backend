from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.serializers.stock_summary_serializer import StockSummarySerializer
from dashboard.repositories.dashboard_repository import DashboardRepository

class StockSummaryView(APIView):
    serializer = StockSummarySerializer
    repository = DashboardRepository
    service = DashboardService(repository)

    @swagger_auto_schema(
        responses={200: StockSummarySerializer}
    )
    def get(self, request):
        stock_summary_data = self.service.get_stock_summary()
        serializer = self.serializer(stock_summary_data)
        return Response(serializer.data, status=status.HTTP_200_OK)