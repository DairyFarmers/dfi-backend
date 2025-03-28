from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from orders.serializers.order_add_serializer import OrderAddSerializer
from orders.services.order_service import OrderService
from orders.models.order import Order
from orders.repositories.order_repository import OrderRepository

class OrderAddView(APIView):
    serializer = OrderAddSerializer
    repository = OrderRepository(Order)
    service = OrderService(repository)

    @swagger_auto_schema(responses={200: OrderAddSerializer})
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            order = self.service.add_order(serializer.validated_data)
            if order:
                return Response({"id": order.id}, status=status.HTTP_201_CREATED)
            return Response({"error": "Order not added"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)