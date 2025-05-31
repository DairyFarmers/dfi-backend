from typing import Any, List, Optional, Type, TypeVar
from django.db.models import Model, QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from exceptions import DatabaseException

T = TypeVar('T', bound=Model)

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, data: dict) -> T:
        try:
            return self.model.objects.create(**data)
        except DatabaseError as e:
            raise DatabaseException(f"Failed to create {self.model.__name__}: {str(e)}")

    def update(self, instance_id: Any, data: dict) -> T:
        try:
            instance = self.get_by_id(instance_id)
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except DatabaseError as e:
            raise DatabaseException(f"Failed to update {self.model.__name__}: {str(e)}")

    def delete(self, instance_id: Any) -> bool:
        try:
            instance = self.get_by_id(instance_id)
            instance.delete()
            return True
        except DatabaseError as e:
            raise DatabaseException(f"Failed to delete {self.model.__name__}: {str(e)}")

    def get_by_id(self, instance_id: Any) -> T:
        try:
            instance = self.model.objects.get(id=instance_id)
            return instance
        except ObjectDoesNotExist:
            raise DatabaseException(f"{self.model.__name__} not found")
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch {self.model.__name__}: {str(e)}")

    def get_all(self, filters: Optional[dict] = None) -> QuerySet[T]:
        try:
            queryset = self.model.objects.all()
            if filters:
                queryset = queryset.filter(**filters)
            return queryset
        except DatabaseError as e:
            raise DatabaseException(f"Failed to fetch {self.model.__name__} list: {str(e)}")

    def exists(self, filters: dict) -> bool:
        try:
            return self.model.objects.filter(**filters).exists()
        except DatabaseError as e:
            raise DatabaseException(f"Failed to check {self.model.__name__} existence: {str(e)}")

    def count(self, filters: Optional[dict] = None) -> int:
        try:
            queryset = self.model.objects.all()
            if filters:
                queryset = queryset.filter(**filters)
            return queryset.count()
        except DatabaseError as e:
            raise DatabaseException(f"Failed to count {self.model.__name__}: {str(e)}")