from repositories.base_repository import BaseRepository
from users.models.passcode import Passcode
from django.db import models, DatabaseError
from exceptions.exceptions import DatabaseException

class PasscodeRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
        
    def get_by_id(self, id):
        try: 
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist: 
            raise DatabaseException('Passcode not found')
        except DatabaseError as e:
            raise DatabaseException('Error retrieving passcode')

    def get_all(self):
        try:
            return self.model.objects.all()
        except DatabaseError as e:
            raise DatabaseException('Error retrieving passcodes')
    
    def get_by_passcode(self, passcode):
        try: 
            return self.model.objects.get(passcode=passcode)
        except self.model.DoesNotExist: 
            raise DatabaseException('Passcode not found')
        except DatabaseError as e:
            raise DatabaseException('Error retrieving passcodes')
    
    def create(self, data):
        try:
            return self.model.objects.create(**data)
        except DatabaseError as e:
            raise DatabaseException('Error creating passcode')

    def update(self, id, **kwargs):
        try:
            instance = self.get_by_id(id)
            if not instance: return None
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except DatabaseError as e:
            raise DatabaseException('Error updating passcode')

    def delete(self, passcode):
        try:
            instance = self.get_by_passcode(passcode)
            if not instance: return False
            instance.delete()
            return True
        except DatabaseError as e:
            raise DatabaseException('Error deleting passcode')