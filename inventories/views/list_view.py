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

            # Handle inactive items
            if not request.query_params.get('include_inactive', False):
                queryset = queryset.filter(is_active=True)

            serializer = self.inventoryItemListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching inventory items: {e}")
            return Response({"error": "Failed to fetch inventory items"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Create a new inventory item",
        request_body=InventoryItemCreateUpdateSerializer,
        responses={201: InventoryItemCreateUpdateSerializer}
    )
    def post(self, request):
        """Create a new inventory item"""
        try:
            print("Request data:", request.data)
            serializer = self.inventoryItemCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                item = self.service.add_item(serializer.validated_data)
                return Response(self.inventoryItemCreateUpdateSerializer(item).data, status=status.HTTP_201_CREATED)
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating inventory item: {e}")
            return Response({"error": "Failed to create inventory item"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 