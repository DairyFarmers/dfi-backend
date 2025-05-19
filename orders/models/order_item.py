from django.db import models
from django.core.validators import MinValueValidator
from .base_model import BaseModel
from .order import Order
from inventories.models import InventoryItem

class OrderItem(BaseModel):
    """
    Model for individual items within an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['inventory_item'])
        ]

    def __str__(self):
        return f"{self.inventory_item.name} - {self.quantity} units"

    def save(self, *args, **kwargs):
        """Calculate total price before saving"""
        self.total_price = (self.quantity * self.unit_price) - self.discount
        super().save(*args, **kwargs)

    def can_modify_quantity(self):
        """Check if the item quantity can be modified"""
        return self.order.can_modify()

    def get_total_weight(self):
        """Calculate total weight of the order item"""
        return self.quantity * self.inventory_item.weight if self.inventory_item.weight else 0 