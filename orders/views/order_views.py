from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from django.db import transaction
from django.core.paginator import Paginator
from orders.models import Order
from orders.serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateUpdateSerializer
)
from orders.repositories import OrderRepository
from .filters import OrderFilter
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    repository_class = OrderRepository
    
    def get_queryset(self):
        try:
            return Order.objects.filter(
                is_active=True
            ).prefetch_related('items').order_by('-created_at')
        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            return Order.objects.none()
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            fetch_all = request.query_params.get('all', '').lower() == 'true'
            
            if fetch_all:
                serializer = self.get_serializer(queryset, many=True)
                return Response({
                    'status': True,
                    'message': 'Orders fetched successfully',
                    'data': {
                        'orders': {
                            'results': serializer.data,
                            'count': queryset.count(),
                        },
                        'stats': {
                            'pending': queryset.filter(status='pending').count(),
                            'completed': queryset.filter(status='delivered').count(),
                            'totalRevenue': queryset.filter(
                                status='delivered'
                            ).aggregate(total=Sum('total_amount'))['total'] or 0
                        }
                    }
                })
            
            page = request.query_params.get('page', 1)
            page_size = int(request.query_params.get('size', 10))
            paginator = Paginator(queryset, page_size)
            current_page = paginator.get_page(page)
            serializer = self.get_serializer(
                current_page.object_list, 
                many=True
            )
            return Response({
                'status': True,
                'message': 'Orders fetched successfully',
                'data': {
                    'orders': {
                        'results': serializer.data,
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'next': current_page.number + 1 if current_page.has_next() else None,
                        'previous': current_page.number - 1 if current_page.has_previous() else None
                    },
                    'stats': {
                        'pending': queryset.filter(status='pending').count(),
                        'completed': queryset.filter(status='delivered').count(),
                        'totalRevenue': queryset.filter(
                            status='delivered'
                        ).aggregate(total=Sum('total_amount'))['total'] or 0
                    }
                }
            })
        except Exception as e:
            logger.error(f"Error listing orders: {str(e)}")
            return Response({
                'message': 'Failed to fetch orders'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderDetailSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"{request.user} is creating an order")
            serializer = self.get_serializer(data=request.data)
    
            if serializer.is_valid():
                try:
                    order = serializer.save()
                    order.calculate_total()
                    return Response({
                        'status': True,
                        'message': 'Order created successfully',
                        'data': OrderDetailSerializer(order).data
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Error saving order: {str(e)}")
                    return Response(
                        {'message': 'Failed to save order'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
    
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return Response(
                {'message': 'Failed to create order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def perform_update(self, serializer):
        try:
            logger.info(
                f"{self.request.user} is updating order {serializer.instance.id}"
            )
            serializer.save()
            order = serializer.instance
            order.calculate_total()
        except Exception as e:
            logger.error(f"Error updating order {serializer.instance.id}: {str(e)}")
            raise e

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        try:
            logger.info(f"{request.user} is cancelling order {pk}")
            order = self.get_object()

            if not order.can_cancel():
                return Response(
                    {"message": "Order cannot be cancelled in its current state"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = 'cancelled'
            order.save()
            logger.info(f"Order {pk} cancelled successfully")
            return Response({
                "status": True,
                "message": "Order cancelled successfully"
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            logger.error(f"Order {pk} not found")
            return Response(
                {"message": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error cancelling order {pk}: {str(e)}")
            return Response(
                {"message": "Failed to cancel order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        """Mark an order as delivered"""
        try:
            logger.info(f"{request.user} is marking order {pk} as delivered")
            order = self.get_object()

            if order.status != 'shipped':
                logger.warning(f"Order {pk} cannot be marked as delivered")
                return Response(
                    {"message": "Only shipped orders can be marked as delivered"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = 'delivered'
            order.actual_delivery_date = timezone.now().date()
            order.save()
            logger.info(f"Order {pk} marked as delivered successfully")
            return Response({
                "status": True,
                "message": "Order marked as delivered"
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            logger.error(f"Order {pk} not found")
            return Response(
                {"message": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error marking order {pk} as delivered: {str(e)}")
            return Response(
                {"message": "Failed to mark order as delivered"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get order statistics"""
        try:
            logger.info(f"{request.user} is fetching order statistics")
            repository = self.repository_class()
            days = int(request.query_params.get('days', 30))
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)
            stats = repository.get_order_statistics(start_date, end_date)
            return Response({
                'status': True,
                'message': 'Order statistics fetched successfully',
                'data': stats
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching order statistics: {str(e)}")
            return Response(
                {"message": "Failed to fetch order statistics"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue orders"""
        try:
            logger.info(f"{request.user} is fetching overdue orders")
            repository = self.repository_class()
            orders = repository.get_overdue_orders()
            serializer = OrderListSerializer(orders, many=True)
            return Response({
                'status': True,
                'message': 'Overdue orders fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching overdue orders: {str(e)}")
            return Response(
                {"message": "Failed to fetch overdue orders"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get orders for a specific customer"""
        try:
            logger.info(f"{request.user} is fetching orders by customer")
            repository = self.repository_class()
            customer_email = request.query_params.get('email')
            
            if not customer_email:
                return Response(
                    {"message": "Customer email is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            orders = repository.get_customer_orders(customer_email)
            stats = repository.get_customer_statistics(customer_email)

            return Response({
                'status': True,
                'message': 'Orders by customer fetched successfully',
                'data': {
                    'orders': OrderListSerializer(orders, many=True).data,
                    'statistics': stats
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching orders by customer: {str(e)}")
            return Response(
                {"message": "Failed to fetch orders by customer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def high_value(self, request):
        """Get high-value orders"""
        try:
            logger.info(f"{request.user} is fetching high-value orders")
            repository = self.repository_class()
            threshold = float(request.query_params.get('threshold', 1000.0))
            orders = repository.get_high_value_orders(threshold)
            serializer = OrderListSerializer(orders, many=True)
            return Response({
                'status': True,
                'message': 'High-value orders fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching high-value orders: {str(e)}")
            return Response(
                {"message": "Failed to fetch high-value orders"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )