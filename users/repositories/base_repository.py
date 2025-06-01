from typing import TypeVar, Type, List, Optional
from django.db.models import Model, QuerySet
from django.core.exceptions import ObjectDoesNotExist

T = TypeVar('T', bound=Model)

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def get_by_id(self, id) -> Optional[T]:
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> bool:
        instance.delete()
        return True

    def filter(self, **kwargs) -> QuerySet[T]:
        return self.model.objects.filter(**kwargs)