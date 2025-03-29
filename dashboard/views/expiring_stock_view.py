from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.serializers.expiring_stock_serializer import ExpiringStockSerializer
from dashboard.repositories.dashboard_repository import DashboardRepository

class ExpiringStockView(APIView):
    serializer = ExpiringStockSerializer
    repository = DashboardRepository
    service = DashboardService(repository)

    @swagger_auto_schema(
        responses={200: ExpiringStockSerializer(many=True)}
    )
    def get(self, request):
        expiring_stock_data = self.service.get_expiring_stock()
        serializer = self.serializer(expiring_stock_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)