from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from django.db import transaction

from orders.models import Order
from orders.serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateUpdateSerializer
)
from orders.repositories import OrderRepository
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    """
    #permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    repository_class = OrderRepository
    
    def get_queryset(self):
        return Order.objects.filter(is_active=True).prefetch_related('items')

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderDetailSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                order = serializer.save()
                order.calculate_total()  # Calculate totals after creating items
                return Response(
                    OrderDetailSerializer(order).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        print("serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()
        order = serializer.instance
        order.calculate_total()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        if not order.can_cancel():
            return Response(
                {"detail": "Order cannot be cancelled in its current state"},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'cancelled'
        order.save()
        return Response({"detail": "Order cancelled successfully"})

    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        """Mark an order as delivered"""
        order = self.get_object()
        if order.status != 'shipped':
            return Response(
                {"detail": "Only shipped orders can be marked as delivered"},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'delivered'
        order.actual_delivery_date = timezone.now().date()
        order.save()
        return Response({"detail": "Order marked as delivered"})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get order statistics"""
        repository = self.repository_class()
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        stats = repository.get_order_statistics(start_date, end_date)
        return Response(stats)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue orders"""
        repository = self.repository_class()
        orders = repository.get_overdue_orders()
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get orders for a specific customer"""
        repository = self.repository_class()
        customer_email = request.query_params.get('email')
        if not customer_email:
            return Response(
                {"detail": "Customer email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = repository.get_customer_orders(customer_email)
        stats = repository.get_customer_statistics(customer_email)
        
        return Response({
            'statistics': stats,
            'orders': OrderListSerializer(orders, many=True).data
        })

    @action(detail=False, methods=['get'])
    def high_value(self, request):
        """Get high-value orders"""
        repository = self.repository_class()
        threshold = float(request.query_params.get('threshold', 1000.0))
        orders = repository.get_high_value_orders(threshold)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data) 