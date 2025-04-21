from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.serializers.sales_graph_serializer import SalesGraphSerializer
from dashboard.repositories.dashboard_repository import DashboardRepository

class SalesGraphView(APIView):
    serializer = SalesGraphSerializer
    repository = DashboardRepository
    service = DashboardService(repository)

    @swagger_auto_schema(
        responses={200: SalesGraphSerializer(many=True)}
    )
    def get(self, request):
        sales_graph_data = self.service.get_sales_graph_data()
        serializer = self.serializer(sales_graph_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)