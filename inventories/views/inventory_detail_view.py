from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from inventories.services.inventory_service import InventoryService
from inventories.serializers.inventory_update_serializer import InventoryUpdateSerializer
from inventories.models.inventory_item import InventoryItem
from inventories.repositories.inventory_repository import InventoryRepository

class InventoryDetailView(APIView):
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

    @swagger_auto_schema(responses={200: InventoryUpdateSerializer()})
    def get(self, request, item_id):
        item = self.service.get_item_by_id(item_id)
        if item:
            serializer = self.serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=InventoryUpdateSerializer, responses={200: "Item updated"})
    def put(self, request, item_id):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            item = self.service.update_item(item_id, serializer.validated_data)
            if item:
                return Response({"message": "Item updated"}, status=status.HTTP_200_OK)
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        deleted = self.service.delete_item(item_id)
        if deleted:
            return Response({"message": "Item deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)