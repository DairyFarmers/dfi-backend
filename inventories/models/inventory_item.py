from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .base_model import BaseModel
import uuid

class InventoryItem(BaseModel):
    DAIRY_TYPE_CHOICES = [
        ('milk', 'Milk'),
        ('cheese', 'Cheese'),
        ('butter', 'Butter'),
        ('yogurt', 'Yogurt'),
        ('cream', 'Cream'),
        ('other', 'Other'),
    ]

    STORAGE_CONDITION_CHOICES = [
        ('refrigerated', 'Refrigerated'),
        ('frozen', 'Frozen'),
        ('room_temp', 'Room Temperature'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dairy_type = models.CharField(max_length=20, choices=DAIRY_TYPE_CHOICES)
    batch_number = models.CharField(max_length=50, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    manufacturing_date = models.DateField()
    storage_condition = models.CharField(
        max_length=20, 
        choices=STORAGE_CONDITION_CHOICES
    )
    is_active = models.BooleanField(default=True)
    
    # Temperature monitoring
    current_temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    optimal_temperature_min = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(-30), MaxValueValidator(30)]
    )
    optimal_temperature_max = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(-30), MaxValueValidator(30)]
    )

    # Stock management
    reorder_point = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Quantity at which to reorder"
    )
    minimum_order_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Minimum quantity that can be ordered"
    )

    # Relationships
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.PROTECT,
        related_name='inventory_items'
    )

    def __str__(self):
        return f"{self.name} - {self.batch_number}"

    class Meta:
        ordering = ['name', '-expiry_date']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['batch_number']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['dairy_type']),
        ]

    @property
    def current_stock(self):
        return self.quantity
    
    @current_stock.setter 
    def current_stock(self, value):
        self.quantity = value

    def update_stock(self, amount: float, action: str = 'add'):
        if action == 'add':
            self.quantity += amount
        elif action == 'subtract':
            if self.quantity >= amount:
                self.quantity -= amount
            else:
                raise ValueError(f"Insufficient stock. Available: {self.quantity}, Requested: {amount}")
        self.save()

    def is_low_stock(self):
        return self.quantity <= self.reorder_point

    def is_temperature_alert(self):
        if self.current_temperature is None:
            return False
        return not (self.optimal_temperature_min <= self.current_temperature <= self.optimal_temperature_max)

    def days_until_expiry(self):
        from django.utils import timezone
        today = timezone.now().date()
        return (self.expiry_date - today).days

    def soft_delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()
