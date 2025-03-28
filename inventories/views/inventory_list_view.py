from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from inventories.models.inventory_item import InventoryItem
from inventories.repositories.inventory_repository import InventoryRepository
from inventories.services.inventory_service import InventoryService
from inventories.serializers.inventory_item_serializer import InventoryItemSerializer

class InventoryListView(APIView):
    serializer = InventoryItemSerializer
    repository = InventoryRepository(InventoryItem)
    service = InventoryService(repository)

    @swagger_auto_schema(responses={200: InventoryItemSerializer(many=True)})
    def get(self, request):
        items = self.service.get_all_items()
        serializer = self.serializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)