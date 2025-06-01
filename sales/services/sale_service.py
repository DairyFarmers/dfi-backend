from django.db import transaction
from django.utils import timezone
from sales.repositories.sale_repository import SaleRepository
from orders.repositories.order_repository import OrderRepository
from inventories.repositories.inventory_repository import InventoryRepository
from orders.models import Order
from inventories.models import InventoryItem

class SaleService:
    def __init__(self):
        self.sale_repository = SaleRepository()
        self.order_repository = OrderRepository(Order)
        self.inventory_repository = InventoryRepository(InventoryItem)

    def get_sales(self, filters=None):
        """Get all sales with optional filtering"""
        return self.sale_repository.get_all_sales(filters=filters)

    def get_sale(self, sale_id):
        """Get a single sale by ID"""
        return self.sale_repository.get_sale_by_id(sale_id)

    @transaction.atomic
    def create_sale(self, order_id, sale_data, user):
        """Create a new sale from an order"""
        if not order_id:
            raise ValueError("Order ID is required")
        
        if isinstance(order_id, str):
                order_id = int(order_id)
        
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order not found with ID: {order_id}")

        if hasattr(order, 'sale'):
            raise ValueError("Sale already exists for this order")

        # Generate invoice number
        current_time = timezone.now()
        sale_data.update({
            'invoice_number': f"INV-{current_time.strftime('%Y%m%d')}-{order.id}",
            'order': order,
            'seller': user,
            'sale_date': current_time,  # Set the sale_date
            'created_by': user,
            'updated_by': user
        })
        
        # Calculate amounts
        subtotal = order.total_amount
        tax_amount = sale_data.get('tax_amount', 0)
        shipping_cost = sale_data.get('shipping_cost', 0)
        discount_amount = sale_data.get('discount_amount', 0)
        
        sale_data['total_amount'] = subtotal + tax_amount + shipping_cost - discount_amount

        # Create sale
        sale = self.sale_repository.create_sale(sale_data, user)

        # Update inventory
        for item in order.items.all():
            inventory_item = item.inventory_item
            inventory_item.quantity -= item.quantity
            inventory_item.save()

        return sale

    @transaction.atomic
    def update_sale(self, sale_id, sale_data, user):
        """Update an existing sale"""
        sale = self.sale_repository.get_sale_by_id(sale_id)
        if not sale:
            raise ValueError("Sale not found")

        # Recalculate total if necessary components changed
        if any(key in sale_data for key in ['tax_amount', 'shipping_cost', 'discount_amount']):
            subtotal = sale.order.total_amount
            tax_amount = sale_data.get('tax_amount', sale.tax_amount)
            shipping_cost = sale_data.get('shipping_cost', sale.shipping_cost)
            discount_amount = sale_data.get('discount_amount', sale.discount_amount)
            sale_data['total_amount'] = subtotal + tax_amount + shipping_cost - discount_amount

        return self.sale_repository.update_sale(sale_id, sale_data, user)

    @transaction.atomic
    def delete_sale(self, sale_id, user):
        """Soft delete a sale"""
        return self.sale_repository.delete_sale(sale_id, user)

    def get_sales_analytics(self, filters=None):
        """Get sales statistics with optional filtering"""
        return self.sale_repository.get_sales_stats(filters)

    # Payment related methods
    @transaction.atomic
    def add_payment(self, sale_id, payment_data, user):
        """Add a payment to a sale"""
        sale = self.sale_repository.get_sale_by_id(sale_id)
        if not sale:
            raise ValueError("Sale not found")

        payment_data['sale'] = sale
        payment = self.sale_repository.add_payment(payment_data, user)
        
        # Update sale payment status
        sale.update_payment_status()
        
        return payment

    def get_sale_payments(self, sale_id, filters=None):
        """Get all payments for a sale with optional filtering"""
        return self.sale_repository.get_sale_payments(sale_id, filters)

    def get_payment_analytics(self, sale_id):
        """Get payment statistics for a sale"""
        return self.sale_repository.get_payment_stats(sale_id)