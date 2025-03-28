from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from orders.serializers.order_serializer import OrderSerializer
from orders.services.order_service import OrderService
from orders.models.order import Order
from orders.repositories.order_repository import OrderRepository

class OrderListView(APIView):
    serializer = OrderSerializer
    repository = OrderRepository(Order)
    service = OrderService(repository)

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = self.service.get_all_orders()
        serializer = self.serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)