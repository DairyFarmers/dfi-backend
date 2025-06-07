from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from inventories.models import InventoryItem
from sales.models import Sale
from orders.models import Order
from utils import setup_logger

logger = setup_logger(__name__)

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query = request.query_params.get('query', '').strip()
            
            if not query:
                return Response({'data': []})

            # Search inventory items
            inventory_items = InventoryItem.objects.filter(
                Q(name__icontains=query) |
                Q(batch_number__icontains=query) |
                Q(dairy_type__icontains=query) |
                Q(description__icontains=query)
            ).select_related('supplier')[:5]

            results = []

            if inventory_items.exists():
                results.append({
                    'type': 'Inventory',
                    'items': [{
                        'id': str(item.id),
                        'type': 'inventory',
                        'title': item.name,
                        'subtitle': f'{item.quantity} {item.unit} - {item.dairy_type}',
                        'metadata': {
                            'batch_number': item.batch_number,
                            'supplier': item.supplier.name if item.supplier else None,
                            'storage': item.storage_condition,
                        },
                        'url': f'/inventory/{item.id}'
                    } for item in inventory_items]
                })

            # Search orders with more fields
            orders = Order.objects.filter(
                Q(id__icontains=query) |
                Q(customer_name__icontains=query) |
                Q(status__icontains=query) |
                Q(shipping_address__icontains=query)
            ).select_related('customer')[:5]

            if orders.exists():
                results.append({
                    'type': 'Orders',
                    'items': [{
                        'id': str(order.id),
                        'type': 'order',
                        'title': f'Order #{str(order.id)[:8]}',
                        'subtitle': f'{order.customer_name} - {order.status}',
                        'metadata': {
                            'total_amount': str(order.total_amount),
                            'date': order.created_at.strftime('%Y-%m-%d'),
                            'status': order.status
                        },
                        'url': f'/sales/orders/{order.id}'
                    } for order in orders]
                })

            # Search sales with related fields
            sales = Sale.objects.filter(
                Q(id__icontains=query) |
                Q(seller__email__icontains=query) |
                Q(payment_status__icontains=query) |
                Q(order__customer_name__icontains=query)
            ).select_related('order', 'seller')[:5]

            if sales.exists():
                results.append({
                    'type': 'Sales',
                    'items': [{
                        'id': str(sale.id),
                        'type': 'sale',
                        'title': f'Sale #{str(sale.id)[:8]}',
                        'subtitle': f'{sale.order.customer_name if sale.order else "N/A"}',
                        'metadata': {
                            'amount': str(sale.order.total_amount if sale.order else 0),
                            'seller': sale.seller.email if sale.seller else 'Unknown',
                            'status': sale.payment_status,
                            'date': sale.created_at.strftime('%Y-%m-%d')
                        },
                        'url': f'/sales/{sale.id}'
                    } for sale in sales]
                })

            return Response({
                'status': True,
                'message': 'Search results retrieved successfully',
                'data': results
            })

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return Response({
                'status': False,
                'message': 'Failed to perform search',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)