from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from suppliers.models import Supplier
from suppliers.serializers import (
    SupplierListSerializer,
    SupplierCreateUpdateSerializer
)
from suppliers.services import SupplierService
from suppliers.views.filters import SupplierFilter
from utils import setup_logger

logger = setup_logger(__name__)

class SupplierListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierListSerializer
    service = SupplierService()

    def get(self, request):
        """Get list of suppliers with filtering"""
        try:
            logger.info(f"{request.user} is retrieving suppliers")
            queryset = self.service.get_all_suppliers()
            
            # Apply filters
            supplier_filter = SupplierFilter(request)
            queryset = supplier_filter.apply_filters(queryset)

            # Handle inactive suppliers
            if not request.query_params.get('include_inactive', False):
                queryset = queryset.filter(is_active=True)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching suppliers: {e}")
            return Response(
                {"error": "Failed to fetch suppliers"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Create a new supplier",
        request_body=SupplierCreateUpdateSerializer,
        responses={201: SupplierListSerializer}
    )
    def post(self, request):
        """Create a new supplier"""
        try:
            logger.info(f"{request.user} is creating a new supplier")
            serializer = SupplierCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                supplier = self.service.create_supplier(serializer.validated_data)
                return Response(
                    self.serializer_class(supplier).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating supplier: {e}")
            return Response(
                {"error": "Failed to create supplier"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )