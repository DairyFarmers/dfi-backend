from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from sales.models import Payment
from sales.services.payment_service import PaymentService
from sales.filters import PaymentFilter
from sales.serializers import (
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    PaymentListSerializer
)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_active=True)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'amount']
    search_fields = ['reference_number', 'sale__invoice_number']
    payment_service = PaymentService()

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action == 'list':
            return PaymentListSerializer
        return PaymentDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Create payment and update sale status
            payment = self.payment_service.create_payment(
                sale_id=request.data.get('sale_id'),
                payment_data={
                    **serializer.validated_data,
                    'payment_date': serializer.validated_data.get('payment_date', timezone.now())
                },
                user=request.user
            )
            response_serializer = PaymentDetailSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def void(self, request, pk=None):
        """Void a payment and update sale status"""
        try:
            payment = self.payment_service.void_payment(pk, request.user)
            serializer = PaymentDetailSerializer(payment)
            return Response(serializer.data)
        except ValueError as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get payment summary for a sale"""
        sale_id = request.query_params.get('sale_id')
        if not sale_id:
            return Response(
                {'error': 'sale_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        summary = self.payment_service.get_payment_summary(sale_id)
        return Response(summary)