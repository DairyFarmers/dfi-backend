from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.serializers.orders_overview_serializer import OrdersOverviewSerializer
from dashboard.repositories.dashboard_repository import DashboardRepository

class OrdersOverviewView(APIView):
    serializer = OrdersOverviewSerializer
    repository = DashboardRepository
    service = DashboardService(repository)

    @swagger_auto_schema(
        responses={200: OrdersOverviewSerializer}
    )
    def get(self, request):
        orders_overview_data = self.service.get_orders_overview()
        serializer = self.serializer(orders_overview_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
