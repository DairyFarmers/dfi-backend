from django.utils import timezone
import random
from exceptions.exceptions import (
    InvalidDataException, 
    RepositoryException, 
    ServiceException
)

class PasscodeService:
    def __init__(self, repository):
        self.repository = repository

    def create_passcode(self, data):
        try:
            self.repository.create(data)
        except RepositoryException as e:
            raise ServiceException('Passcode creation failed')
        
    def get_passcode(self, passcode):
        try:
            return self.repository.get_by_passcode(passcode)
        except RepositoryException as e:
            raise ServiceException('Passcode not found')
        
    def delete_passcode(self, passcode):
        try:
            self.repository.delete(passcode)
        except RepositoryException as e:
            raise ServiceException('Passcode deletion failed')

    def valid_passcode(self, passcode):
        return timezone.now() < passcode.expires_at
    
    def generate_passcode(self, length=8):
        return ''.join(random.choices('0123456789', k=length))
        
        
