from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from orders.serializers.order_update_serializer import OrderUpdateSerializer
from orders.services.order_service import OrderService
from orders.models.order import Order
from orders.repositories.order_repository import OrderRepository

class OrderDetailView(APIView):
    serializer = OrderUpdateSerializer
    repository = OrderRepository(Order)
    service = OrderService(repository)

    @swagger_auto_schema(responses={200: OrderUpdateSerializer})
    def get(self, request, order_id):
        order = self.service.get_order_by_id(order_id)
        if order:
            serializer = self.serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=OrderUpdateSerializer, responses={200: "Order Updated"})
    def put(self, request, order_id):
        data = request.data
        if self.service.update_order(order_id, **data):
            return Response({"message": "Order updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, order_id):
        if self.service.delete_order(order_id):
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)