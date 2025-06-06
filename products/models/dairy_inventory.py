from django.db import models
from products.models import BaseModel

class DairyInventory(BaseModel):
    production = models.ForeignKey(
        'DairyProduction', 
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    batch_number = models.CharField(max_length=50, unique=True)
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    storage_location = models.CharField(max_length=100)
    storage_temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Storage temperature in Celsius"
    )

    class Meta:
        db_table = 'dairy_inventory'
        ordering = ['expiry_date']