from django.db.models import Model
from django.db.models.query import QuerySet
from typing import Optional, Any, TypeVar, Generic

T = TypeVar('T', bound=Model)

class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""
    def __init__(self, model_class: type[T]):
        self.model_class = model_class

    def get_all(self) -> QuerySet[T]:
        """Get all records"""
        return self.model_class.objects.all()

    def get_by_id(self, id: int) -> Optional[T]:
        """Get a record by ID"""
        try:
            return self.model_class.objects.get(id=id)
        except self.model_class.DoesNotExist:
            return None

    def create(self, **kwargs: Any) -> T:
        """Create a new record"""
        return self.model_class.objects.create(**kwargs)

    def update(self, instance: T, **kwargs: Any) -> T:
        """Update an existing record"""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> bool:
        """Delete a record"""
        instance.delete()
        return True

    def filter(self, **kwargs: Any) -> QuerySet[T]:
        """Filter records based on criteria"""
        return self.model_class.objects.filter(**kwargs) 