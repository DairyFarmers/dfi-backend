from repositories.base_repository import BaseRepository
from users.models import User
from django.db import models, DatabaseError
from exceptions.exceptions import DatabaseException

class UserRepository(BaseRepository):
    def __init__(self, model: models.Model):
        super().__init__(model)
    
    def get_by_id(self, user_id):
        try:
            return self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            raise DatabaseException('User not found')
        except DatabaseError as e:
            raise DatabaseException('Error retrieving user')
        
    def get_by_email(self, email):
        try:
            return self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            raise DatabaseException('User not found')
        except DatabaseError as e:
            raise DatabaseException('Error retrieving user')

    def get_all(self):
        try:
            return self.model.objects.all()
        except DatabaseError as e:
            raise DatabaseException('Error retrieving users')
        
    def get_only(self, user_id, *fields):
        try:
            return self.model.objects.only(*fields).get(id=user_id)
        except self.model.DoesNotExist:
            raise DatabaseException('User not found')
        except DatabaseError as e:
            raise DatabaseException('Error retrieving user')
    
    def create(self, data):
        try:
            return self.model.objects.create_user(**data)
        except DatabaseError as e:
            raise DatabaseException('Error creating user')

    def update(self, id, **kwargs):
        try:
            instance = self.get_by_id(id)
            if not instance: return None
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except DatabaseError as e:
            raise DatabaseException('Error updating user')

    def delete(self, id):
        try:
            instance = self.get_by_id(id)
            if not instance: return False
            instance.delete()
            return True
        except DatabaseError as e:
            raise DatabaseException('Error deleting user')