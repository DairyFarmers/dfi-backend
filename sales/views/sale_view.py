from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from sales.models import Sale, Payment
from sales.filters import SaleFilter, PaymentFilter
from sales.serializers import (
    SaleSerializer,
    SaleCreateSerializer,
    PaymentDetailSerializer
)
from sales.services import SaleService
from django.utils import timezone

class SaleViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return SaleCreateSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = SaleService()
        try:
            sale = service.create_sale(
                order_id=request.data.get('order_id'),
                sale_data={
                    **serializer.validated_data,
                    'sale_date': timezone.now()  # Explicitly set sale_date
                },
                user=request.user
            )
            response_serializer = SaleSerializer(sale)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        filters = self.request.query_params
        service = SaleService()
        return service.get_sales(filters=filters)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = PaymentDetailSerializer
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'amount']
    search_fields = ['reference_number', 'sale__invoice_number']