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
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

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
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            fetch_all = request.query_params.get('all', '').lower() == 'true'
            
            if fetch_all:
                serializer = self.get_serializer(queryset, many=True)
                return Response({
                    'status': True,
                    'message': 'Payments fetched successfully',
                    'data': {
                        'results': serializer.data,
                        'count': queryset.count(),
                    }
                })
            
            page = request.query_params.get('page', 1)
            page_size = int(request.query_params.get('size', 10))
            paginator = Paginator(queryset, page_size)
            current_page = paginator.get_page(page)
            serializer = self.get_serializer(
                current_page.object_list, 
                many=True
            )
            return Response({
                'status': True,
                'message': 'Payments fetched successfully',
                'data': {
                    'results': serializer.data,
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'next': current_page.number + 1 if current_page.has_next() else None,
                    'previous': current_page.number - 1 if current_page.has_previous() else None
                }
            })
        except Exception as e:
            logger.error(f"Error listing payments: {str(e)}")
            return Response({
                'message': 'Failed to fetch payments'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info(f"{request.user} is creating a payment")
        
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"Validation error: {serializer.errors}")
                return Response({
                    'status': False,
                    'message': 'Invalid payment data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            payment = self.payment_service.create_payment(
                sale_id=request.data.get('sale_id'),
                payment_data={
                    **serializer.validated_data,
                    'payment_date': serializer.validated_data.get(
                        'payment_date', 
                        timezone.now()
                    )
                },
                user=request.user
            )
            response_serializer = PaymentDetailSerializer(payment)
            return Response({
                'status': True,
                'message': 'Payment created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"Error creating payment: {e}")
            return Response({
                'status': False,
                'message': 'Failed to create payment',
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error creating payment: {e}")
            return Response({
                'status': False,
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'])
    def void(self, request, pk=None):
        """Void a payment and update sale status"""
        try:
            logger.info(f"{request.user} is voiding payment with ID {pk}")
            payment = self.payment_service.void_payment(pk, request.user)
            serializer = PaymentDetailSerializer(payment)
            return Response({
                'status': True,
                'message': 'Payment voided successfully',
                'data': serializer.data
            })
        except ValueError as e:
            logger.error(f"Error voiding payment: {e}")
            return Response({
                'message': 'Failed to void payment',
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error voiding payment: {e}")
            return Response({
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get payment summary for a sale"""
        try:
            logger.info(f"{request.user} is retrieving payment summary")
            sale_id = request.query_params.get('sale_id')
            logger.info(f"Received sale_id: {sale_id}")
            
            if not sale_id:
                logger.error("sale_id is required for payment summary")
                return Response({
                    'message': 'sale_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            summary = self.payment_service.get_payment_summary(sale_id)
            return Response({
                'status': True,
                'message': 'Payment summary fetched successfully',
                'data': summary
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Error retrieving payment summary: {e}")
            return Response({
                'message': 'Failed to retrieve payment summary',
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error retrieving payment summary: {e}")
            return Response({
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)