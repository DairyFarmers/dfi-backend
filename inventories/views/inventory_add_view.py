from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from inventories.services.inventory_service import InventoryService
from inventories.serializers.inventory_update_serializer import InventoryUpdateSerializer
from inventories.models.inventory_item import InventoryItem
from inventories.repositories.inventory_repository import InventoryRepository

class InventoryAddView(APIView):
    serializer = InventoryUpdateSerializer
    repository = InventoryRepository(InventoryItem)
    service = InventoryService(repository)

    @swagger_auto_schema(request_body=InventoryUpdateSerializer, responses={201: "Item created"})
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            item = self.service.add_item(serializer.validated_data)
            return Response({"id": item.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
