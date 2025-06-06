from django.db import models
from products.models import BaseModel
from users.models import User

class DairyProduction(BaseModel):
    MILK_TYPES = [
        ('raw', 'Raw Milk'),
        ('processed', 'Processed Milk'),
        ('butter', 'Butter'),
        ('cheese', 'Cheese'),
        ('yogurt', 'Yogurt')
    ]

    farmer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='dairy_productions'
    )
    product_type = models.CharField(max_length=20, choices=MILK_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    production_date = models.DateField()
    fat_content = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    protein_content = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    quality_score = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'dairy_production'
        ordering = ['-production_date']