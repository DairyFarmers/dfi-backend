from django.db.models import QuerySet
from typing import Any, Dict, List, Optional, Type, TypeVar

ModelType = TypeVar("ModelType")

class BaseRepository:
    """
    Base repository with common database operations.
    """
    model_class: Type[ModelType]

    def __init__(self):
        if not self.model_class:
            raise ValueError("model_class must be set")

    def get_queryset(self) -> QuerySet:
        """Get the base queryset for the model"""
        return self.model_class.objects.filter(is_active=True)

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID"""
        try:
            return self.get_queryset().get(id=id)
        except self.model_class.DoesNotExist:
            return None

    def get_all(self) -> QuerySet:
        """Get all active records"""
        return self.get_queryset()

    def create(self, data: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        return self.model_class.objects.create(**data)

    def update(self, instance: ModelType, data: Dict[str, Any]) -> ModelType:
        """Update an existing record"""
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance: ModelType) -> bool:
        """Soft delete a record"""
        try:
            instance.soft_delete()
            return True
        except Exception:
            return False

    def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[ModelType]:
        """Create multiple records"""
        instances = [self.model_class(**data) for data in data_list]
        return self.model_class.objects.bulk_create(instances)

    def bulk_update(self, instances: List[ModelType], fields: List[str]) -> int:
        """Update multiple records"""
        return self.model_class.objects.bulk_update(instances, fields)

    def exists(self, **kwargs) -> bool:
        """Check if a record exists"""
        return self.get_queryset().filter(**kwargs).exists() 