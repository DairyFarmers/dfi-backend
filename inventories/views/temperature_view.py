from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from inventories.models import InventoryItem
from inventories.serializers import InventoryItemDetailSerializer
from inventories.services.inventory_service import InventoryService
from inventories.repositories.inventory_repository import InventoryRepository
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

class InventoryItemTemperatureView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryItemDetailSerializer
    repository = InventoryRepository(InventoryItem)
    service = InventoryService(repository)

    @swagger_auto_schema(
        operation_description="Update the temperature of an inventory item",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['temperature'],
            properties={
                'temperature': openapi.Schema(type=openapi.TYPE_NUMBER)
            }
        ),
        responses={
            200: InventoryItemDetailSerializer,
            400: "Invalid temperature value",
            404: "Item not found"
        }
    )
    def post(self, request, pk):
        """Update the temperature of an inventory item"""
        try:
            temperature = float(request.data.get('temperature'))
            item = self.service.update_item_temperature(pk, temperature)
            
            if item and item.is_active:
                serializer = self.serializer_class(item)
                paginator = Paginator(
                    serializer.data,
                    serializer.validated_data['size']
                )
                page_obj = paginator.get_page(serializer.validated_data['page'])
                return Response({
                    "status": True,
                    "message": "Temperature updated successfully",
                    "data": page_obj.object_list,
                    "page": page_obj.number,
                    "pages": paginator.num_pages,
                    "total": paginator.count
                }, status=status.HTTP_200_OK)
            return Response(
                {"message": "Item not found or inactive"},
                status=status.HTTP_404_NOT_FOUND
            )
        except (TypeError, ValueError):
            logger.error(
                f"Invalid temperature value: {request.data.get('temperature')}"
            )
            return Response(
                {"message": "Invalid temperature value"},
                status=status.HTTP_400_BAD_REQUEST
            ) 