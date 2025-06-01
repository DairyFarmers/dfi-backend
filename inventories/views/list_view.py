from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from inventories.models import InventoryItem
from inventories.serializers import (
    InventoryItemListSerializer,
    InventoryItemCreateUpdateSerializer
)
from inventories.services.inventory_service import InventoryService
from inventories.repositories.inventory_repository import InventoryRepository
from inventories.views.filters.inventory_item_filter import InventoryItemFilter
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

class InventoryItemView(APIView):
    permission_classes = [IsAuthenticated]
    inventoryItemListSerializer = InventoryItemListSerializer
    inventoryItemCreateUpdateSerializer = InventoryItemCreateUpdateSerializer
    repository = InventoryRepository(InventoryItem)
    service = InventoryService(repository)

    def get(self, request):
        """Get list of inventory items with filtering"""
        try:
            queryset = self.service.get_all_items()
            item_filter = InventoryItemFilter(request)
            queryset = item_filter.apply_filters(queryset)
            
            if not request.query_params.get('include_inactive', False):
                queryset = queryset.filter(is_active=True)

            fetch_all = request.query_params.get('all', '').lower() == 'true'
            
            if fetch_all:
                serializer = self.inventoryItemListSerializer(queryset, many=True)
                return Response({
                    "status": True,
                    "message": "Inventory items fetched successfully",
                    "data": {
                        'results': serializer.data,
                        'count': queryset.count(),
                    }
                }, status=status.HTTP_200_OK)
            
            page = int(request.query_params.get('page', 1))
            size = int(request.query_params.get('size', 10))
            paginator = Paginator(
                queryset, 
                size if size > 0 else 10
            )
            current_page = paginator.get_page(page)
            serializer = self.inventoryItemListSerializer(
                current_page.object_list, 
                many=True
            )
            
            return Response({
                "status": True,
                "message": "Inventory items fetched successfully",
                "data": {
                    'results': serializer.data,
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'next': page + 1 if current_page.has_next() else None,
                    'previous': page - 1 if current_page.has_previous() else None
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching inventory items: {e}")
            return Response(
                {"message": "Failed to fetch inventory items"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Create a new inventory item",
        request_body=InventoryItemCreateUpdateSerializer,
        responses={201: InventoryItemCreateUpdateSerializer}
    )
    def post(self, request):
        """Create a new inventory item"""
        try:
            print("Request data:", request.data)
            serializer = self.inventoryItemCreateUpdateSerializer(
                data=request.data
            )
            if serializer.is_valid():
                item = self.service.add_item(serializer.validated_data)
                return Response({
                    "status": True,
                    "message": "Inventory item created successfully",
                    "data": self.inventoryItemCreateUpdateSerializer(item).data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating inventory item: {e}")
            return Response({
                "message": "Failed to create inventory item"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 