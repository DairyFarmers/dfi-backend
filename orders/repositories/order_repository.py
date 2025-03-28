from repositories.base_repository import BaseRepository
from django.db import models, DatabaseError
from exceptions.exceptions import DatabaseException

class OrderRepository(BaseRepository):
    def __init__(self, model: models.Model):
        super().__init__(model)

    def get_by_id(self, item_id):
        try:
            return self.model.objects.get(id=item_id)
        except self.model.DoesNotExist:
            raise DatabaseException('Item not found')
        except DatabaseError as e:
            raise DatabaseException('Error while retrieving item')
        
    def get_all(self):
        try:
            return self.model.objects.all()
        except DatabaseError as e:
            raise DatabaseException('Error while retrieving items')
        
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