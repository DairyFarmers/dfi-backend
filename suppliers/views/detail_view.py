from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from suppliers.serializers import (
    SupplierDetailSerializer,
    SupplierCreateUpdateSerializer
)
from suppliers.services import SupplierService

class SupplierDetailView(APIView):
    """View for retrieving, updating and deleting a supplier"""
    serializer_class = SupplierDetailSerializer
    service = SupplierService()

    def get_object(self, pk):
        return self.service.get_supplier_by_id(pk)

    def get(self, request, pk):
        """Get a specific supplier"""
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {"error": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(supplier)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a supplier",
        request_body=SupplierCreateUpdateSerializer,
        responses={
            200: SupplierDetailSerializer,
            404: "Supplier not found",
            400: "Invalid data"
        }
    )
    def put(self, request, pk):
        """Update a supplier"""
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {"error": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = SupplierCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            updated_supplier = self.service.update_supplier(
                pk, serializer.validated_data
            )
            return Response(self.serializer_class(updated_supplier).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a supplier",
        responses={
            204: "Supplier deleted",
            404: "Supplier not found"
        }
    )
    def delete(self, request, pk):
        """Delete a supplier"""
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {"error": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        supplier.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Restore a soft-deleted supplier",
        responses={
            200: SupplierDetailSerializer,
            404: "Supplier not found"
        }
    )
    def post(self, request, pk):
        """Restore a deleted supplier"""
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {"error": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        supplier.restore()
        serializer = self.serializer_class(supplier)
        return Response(serializer.data) 