from django.db import models, DatabaseError
from exceptions.exceptions import DatabaseException
from typing import List, Optional
from datetime import date
from inventories.models import InventoryItem
from utils import setup_logger

class InventoryRepository:
    def __init__(self, model: InventoryItem):
        self.model = model
        self.logger = setup_logger(__name__)

    def get_all(self) -> models.QuerySet:
        self.logger.debug("Fetching all inventory items")
        return self.model.objects.all()

    def get_by_id(self, item_id: int) -> Optional[InventoryItem]:
        try:
            self.logger.debug(f"Fetching inventory item with ID: {item_id}")
            return self.model.objects.get(id=item_id)
        except self.model.DoesNotExist:
            self.logger.error(f"Inventory item with ID {item_id} does not exist")
            return None

    def get_low_stock_items(self) -> models.QuerySet:
        self.logger.debug("Fetching low stock items")
        return self.model.objects.filter(quantity__lte=models.F('reorder_point'))

    def get_expiring_items(self, start_date: date, end_date: date) -> models.QuerySet:
        self.logger.debug(f"Fetching items expiring between {start_date} and {end_date}")
        return self.model.objects.filter(
            expiry_date__lte=end_date,
            expiry_date__gte=start_date
        )

    def get_temperature_alerts(self) -> models.QuerySet:
        self.logger.debug("Fetching items with temperature alerts")
        return self.model.objects.filter(
            current_temperature__isnull=False
        ).exclude(
            current_temperature__gte=models.F('optimal_temperature_min'),
            current_temperature__lte=models.F('optimal_temperature_max')
        )

    def update_temperature(self, item_id: int, temperature: float) -> Optional[InventoryItem]:
        try:
            self.logger.debug(f"Updating temperature for item ID {item_id} to {temperature}")
            item = self.model.objects.get(id=item_id)
            item.current_temperature = temperature
            item.save()
            self.logger.info(f"Temperature updated for item ID {item_id}")
            return item
        except self.model.DoesNotExist:
            self.logger.error(f"Item with ID {item_id} does not exist")
            return None

    def get_only(self, item_id, *fields):
        try:
            self.logger.debug(f"Fetching item with ID {item_id} with fields: {fields}")
            return self.model.objects.only(*fields).get(id=item_id)
        except self.model.DoesNotExist:
            self.logger.error(f"Item with ID {item_id} not found")
            raise DatabaseException('Item not found')
        except DatabaseError as e:
            self.logger.error(f"Database error while retrieving item with ID {item_id}: {e}")
            raise DatabaseException('Error while retrieving item')
    
    def create(self, data):
        try:
            self.logger.debug(f"Creating new inventory item with data: {data}")
            return self.model.objects.create(**data)
        except DatabaseError as e:
            self.logger.error(f"Database error while creating item: {e}")
            raise DatabaseException('Error while adding item')

    def update(self, id, **kwargs):
        try:
            self.logger.debug(f"Updating item with ID {id} with data: {kwargs}")
            instance = self.get_by_id(id)
            if not instance: return None
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            self.logger.info(f"Item with ID {id} updated successfully")
            return instance
        except DatabaseError as e:
            self.logger.error(f"Database error while updating item with ID {id}: {e}")
            raise DatabaseException('Error while updating item')

    def delete(self, id):
        try:
            self.logger.debug(f"Deleting item with ID {id}")
            instance = self.get_by_id(id)
            if not instance: return False
            instance.delete()
            self.logger.info(f"Item with ID {id} deleted successfully")
            return True
        except DatabaseError as e:
            self.logger.error(f"Database error while deleting item with ID {id}: {e}")
            raise DatabaseException('Error while deleting item')