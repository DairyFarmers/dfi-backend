from django.db import models
from repositories.interfaces.base_repository_interface \
    import BaseRepositoryInterface
from exceptions.exceptions import DatabaseException

class BaseRepository(BaseRepositoryInterface):
    def __init__(self, model: models.Model):
        self.model = model
        
    def get_all(self):
        try:
            return self.model.objects.all()
        except DatabaseError as e:
            raise DatabaseException('Error retrieving data')

    def get(self, **kwargs):
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            raise DatabaseException('Data not found')

    def filter(self, **kwargs):
        try:
            return self.model.objects.filter(**kwargs)
        except DatabaseError as e:
            raise DatabaseException('Error retrieving data')

    def create(self, **kwargs):
        try:
            return self.model.objects.create(**kwargs)
        except DatabaseError as e:
            raise DatabaseException('Error creating data')

    def update(self, instance, **kwargs):
        try:
            instance = self.get_by_id(id)
            if not instance: return None
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except DatabaseError as e:
            raise DatabaseException('Error updating data')

    def delete(self, instance):
        try:
            instance = self.get_by_id(id)
            if not instance: return False
            instance.delete()
            return True
        except DatabaseError as e:
            raise DatabaseException('Error deleting data')