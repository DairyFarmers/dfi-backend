from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from inventories.models import InventoryItem
from inventories.serializers import (
    InventoryItemDetailSerializer,
    InventoryItemCreateUpdateSerializer
)
from inventories.services.inventory_service import InventoryService
from inventories.repositories.inventory_repository import InventoryRepository
from utils import setup_logger

logger = setup_logger(__name__)

class InventoryItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryItemDetailSerializer
    repository = InventoryRepository(InventoryItem)
    service = InventoryService(repository)

    def get_object(self, pk):
        item = self.service.get_item_by_id(pk)
        if not item:
            return None
        return item

    def get(self, request, pk):
        """Get a specific inventory item"""
        try:
            item = self.get_object(pk)
            if not item:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(item)

            mock_data = {
                "id": 1,
                "name": "Milk",
                "description": "Fresh cow milk",
                "dairy_type": "Cow",
                "quantity": 9,
                "unit": "Liters",
                "price": 1.5,
                "expiry_date": "2023-12-31",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z"
            }
            return Response(mock_data)
        except Exception as e:
            logger.error(f"Error fetching inventory item: {e}")
            return Response({"error": "Failed to fetch inventory item"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update an inventory item",
        request_body=InventoryItemCreateUpdateSerializer,
        responses={
            200: InventoryItemDetailSerializer,
            404: "Item not found",
            400: "Invalid data"
        }
    )
    def put(self, request, pk):
        """Update an inventory item"""
        try:
            item = self.get_object(pk)
            if not item:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(item, data=request.data)
            if serializer.is_valid():
                updated_item = self.service.update_item(pk, **serializer.validated_data)
                return Response(self.serializer_class(updated_item).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating inventory item: {e}")
            return Response({"error": "Failed to update inventory item"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete an inventory item",
        responses={
            204: "Item deleted",
            404: "Item not found"
        }
    )
    def delete(self, request, pk):
        """Delete an inventory item"""
        try:
            item = self.get_object(pk)
            if not item:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            item.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting inventory item: {e}")
            return Response({"error": "Failed to delete inventory item"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Restore a soft-deleted inventory item",
        responses={
            200: InventoryItemDetailSerializer,
            404: "Item not found"
        }
    )
    def post(self, request, pk):
        """Restore a deleted inventory item"""
        try:
            item = self.get_object(pk)
            if not item:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            item.restore()
            serializer = self.serializer_class(item)
            return Response(serializer.data) 
        except Exception as e:
            logger.error(f"Error restoring inventory item: {e}")
            return Response({"error": "Failed to restore inventory item"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)