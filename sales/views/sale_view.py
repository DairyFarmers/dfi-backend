from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from sales.models import Sale, Payment
from sales.filters import SaleFilter, PaymentFilter
from sales.serializers import (
    SaleSerializer,
    SaleCreateSerializer,
)
from sales.services import SaleService
from django.utils import timezone
from django.core.paginator import Paginator
from utils import setup_logger

logger = setup_logger(__name__)

class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return SaleCreateSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"{request.user} is creating a sale")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = SaleService()

        try:
            sale = service.create_sale(
                order_id=serializer.validated_data.get('order_id'),
                sale_data={
                    **serializer.validated_data,
                    'sale_date': timezone.now()
                },
                user=request.user
            )
            response_serializer = SaleSerializer(sale)
            return Response({
                'status': True,
                'message': 'Sale created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"Error creating sale: {e}")
            return Response({
                'message': 'Failed to create sale',
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error creating sale: {e}")
            return Response({
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_queryset(self):
        try:
            filters = self.request.query_params
            service = SaleService()
            return service.get_sales(filters=filters)
        except Exception as e:
            logger.error(f"Error fetching sales: {str(e)}")
            return Sale.objects.none()
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            fetch_all = request.query_params.get('all', '').lower() == 'true'
            
            if fetch_all:
                serializer = self.get_serializer(queryset, many=True)
                return Response({
                    'status': True,
                    'message': 'Sales fetched successfully',
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
                'message': 'Sales fetched successfully',
                'data': {
                    'results': serializer.data,
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'next': current_page.number + 1 if current_page.has_next() else None,
                    'previous': current_page.number - 1 if current_page.has_previous() else None
                }
            })
        except Exception as e:
            logger.error(f"Error listing orders: {str(e)}")
            return Response({
                'message': 'Failed to fetch orders'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)