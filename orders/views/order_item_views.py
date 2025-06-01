from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import OrderItem
from orders.serializers import (
    OrderItemListSerializer,
    OrderItemDetailSerializer,
    OrderItemCreateUpdateSerializer
)
from orders.repositories import OrderItemRepository
from .filters import OrderItemFilter
from utils import setup_logger

logger = setup_logger(__name__)

class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = OrderItemFilter
    repository_class = OrderItemRepository

    def get_queryset(self):
        return OrderItem.objects.filter(is_active=True)\
            .select_related('order', 'inventory_item')

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderItemListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrderItemCreateUpdateSerializer
        return OrderItemDetailSerializer

    def perform_create(self, serializer):
        serializer.save()
        order = serializer.instance.order
        order.calculate_total()

    def perform_update(self, serializer):
        serializer.save()
        order = serializer.instance.order
        order.calculate_total()

    def perform_destroy(self, instance):
        order = instance.order
        instance.delete()
        order.calculate_total()

    @action(detail=False, methods=['get'])
    def by_order(self, request):
        """Get items for a specific order"""
        try:
            logger.info(f"{request.user} is retrieving order items by order ID")
            repository = self.repository_class()
            order_id = request.query_params.get('order_id')
            if not order_id:
                return Response(
                    {"detail": "Order ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            items = repository.get_items_by_order(order_id)
            serializer = OrderItemListSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving order items: {str(e)}")
            return Response(
                {"detail": "Failed to retrieve order items"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_inventory_item(self, request):
        """Get order items for a specific inventory item"""
        try:
            logger.info(f"{request.user} is retrieving order items by inventory item ID")
            repository = self.repository_class()
            inventory_item_id = request.query_params.get('inventory_item_id')
            if not inventory_item_id:
                return Response(
                    {"detail": "Inventory item ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            items = repository.get_items_by_inventory_item(inventory_item_id)
            stats = repository.calculate_item_statistics(inventory_item_id)
            
            return Response({
                'statistics': stats,
                'items': OrderItemListSerializer(items, many=True).data
            })
        except Exception as e:
            logger.error(f"Error retrieving order items by inventory item: {str(e)}")
            return Response(
                {"detail": "Failed to retrieve order items by inventory item"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def top_selling(self, request):
        """Get top selling items"""
        try:
            logger.info(f"{request.user} is retrieving top selling items")
            repository = self.repository_class()
            limit = int(request.query_params.get('limit', 10))
            items = repository.get_top_selling_items(limit)
            return Response(items)
        except Exception as e:
            logger.error(f"Error retrieving top selling items: {str(e)}")
            return Response(
                {"detail": "Failed to retrieve top selling items"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def most_discounted(self, request):
        """Get items with highest total discounts"""
        try:
            logger.info(f"{request.user} is retrieving most discounted items")
            repository = self.repository_class()
            limit = int(request.query_params.get('limit', 10))
            items = repository.get_most_discounted_items(limit)
            return Response(items)
        except Exception as e:
            logger.error(f"Error retrieving most discounted items: {str(e)}")
            return Response(
                {"detail": "Failed to retrieve most discounted items"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def with_discounts(self, request):
        """Get all items with discounts"""
        try:
            logger.info(f"{request.user} is retrieving items with discounts")
            repository = self.repository_class()
            items = repository.get_discounted_items()
            serializer = OrderItemListSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving items with discounts: {str(e)}")
            return Response(
                {"detail": "Failed to retrieve items with discounts"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )