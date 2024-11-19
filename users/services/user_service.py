from exceptions.exceptions import (
    RepositoryException,
    ServiceException
)

class UserService:
    def __init__(self, repository):
        self.repository = repository
        
    def create_user(self, data):
        try:
            return self.repository.create(data)
        except RepositoryException as e:
            raise ServiceException('User creation failed')