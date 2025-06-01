from exceptions.exceptions import (
    RepositoryException,
    ServiceException
)
from django.utils import timezone
from datetime import timedelta
from django.db import models
from typing import List, Optional
from inventories.repositories.inventory_repository import InventoryRepository
from inventories.models.inventory_item import InventoryItem
from utils import setup_logger

class InventoryService:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository
        self.logger = setup_logger(__name__)

    def get_all_items(self) -> models.QuerySet:
        try:
            return self.repository.get_all()
        except RepositoryException as e:
            self.logger.error(f"Error retrieving items: {e}")
            raise ServiceException('Error while retrieving items')

    def add_item(self, data):
        try:
            return self.repository.create(data)
        except RepositoryException as e:
            self.logger.error(f"Error adding item: {e}")
            raise ServiceException('Error while adding item')
        
    def get_item_by_id(self, item_id: int) -> Optional[InventoryItem]:
        try:
            return self.repository.get_by_id(item_id)
        except RepositoryException as e:
            self.logger.error(f"Error retrieving item with ID {item_id}: {e}")
            raise ServiceException('Item not found')
        
    def update_item(self, item_id, **kwargs):
        try:
            return self.repository.update(item_id, **kwargs)
        except RepositoryException as e:
            self.logger.error(f"Error updating item with ID {item_id}: {e}")
            raise ServiceException('Error while updating item')
        
    def delete_item(self, item_id):
        try:
            return self.repository.delete(item_id)
        except RepositoryException as e:
            self.logger.error(f"Error deleting item with ID {item_id}: {e}")
            raise ServiceException('Error while deleting item')

    def get_low_stock_items(self) -> models.QuerySet:
        """Get items with quantity below or at reorder point"""
        return self.repository.get_low_stock_items()

    def get_expiring_soon_items(self, days: int = 30) -> models.QuerySet:
        """Get items expiring within the specified number of days"""
        today = timezone.now().date()
        end_date = today + timedelta(days=days)
        return self.repository.get_expiring_items(today, end_date)

    def get_temperature_alerts(self) -> models.QuerySet:
        """Get items with temperature outside optimal range"""
        return self.repository.get_temperature_alerts()

    def update_item_temperature(self, item_id: int, temperature: float) -> Optional[InventoryItem]:
        """Update the current temperature of an item"""
        return self.repository.update_temperature(item_id, temperature)