from django.db import models, DatabaseError
from exceptions.exceptions import DatabaseException
from typing import List, Optional
from datetime import date
from inventories.models import InventoryItem

class InventoryRepository:
    def __init__(self, model: InventoryItem):
        self.model = model

    def get_all(self) -> models.QuerySet:
        return self.model.objects.all()

    def get_by_id(self, item_id: int) -> Optional[InventoryItem]:
        try:
            return self.model.objects.get(id=item_id)
        except self.model.DoesNotExist:
            return None

    def get_low_stock_items(self) -> models.QuerySet:
        return self.model.objects.filter(quantity__lte=models.F('reorder_point'))

    def get_expiring_items(self, start_date: date, end_date: date) -> models.QuerySet:
        return self.model.objects.filter(
            expiry_date__lte=end_date,
            expiry_date__gte=start_date
        )

    def get_temperature_alerts(self) -> models.QuerySet:
        return self.model.objects.filter(
            current_temperature__isnull=False
        ).exclude(
            current_temperature__gte=models.F('optimal_temperature_min'),
            current_temperature__lte=models.F('optimal_temperature_max')
        )

    def update_temperature(self, item_id: int, temperature: float) -> Optional[InventoryItem]:
        try:
            item = self.model.objects.get(id=item_id)
            item.current_temperature = temperature
            item.save()
            return item
        except self.model.DoesNotExist:
            return None

    def get_only(self, item_id, *fields):
        try:
            return self.model.objects.only(*fields).get(id=item_id)
        except self.model.DoesNotExist:
            raise DatabaseException('Item not found')
        except DatabaseError as e:
            raise DatabaseException('Error while retrieving item')
    
    def create(self, data):
        try:
            return self.model.objects.create(**data)
        except DatabaseError as e:
            raise DatabaseException('Error while adding item')

    def update(self, id, **kwargs):
        try:
            instance = self.get_by_id(id)
            if not instance: return None
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except DatabaseError as e:
            raise DatabaseException('Error while updating item')

    def delete(self, id):
        try:
            instance = self.get_by_id(id)
            if not instance: return False
            instance.delete()
            return True
        except DatabaseError as e:
            raise DatabaseException('Error while deleting item')