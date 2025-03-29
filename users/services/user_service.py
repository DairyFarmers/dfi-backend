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
        
    def get_user_by_id(self, user_id):
        try:
            return self.repository.get(id=user_id)
        except RepositoryException as e:
            raise ServiceException('User not found')
        
    def get_user_by_email(self, email):
        try:
            return self.repository.get_by_email(email=email)
        except RepositoryException as e:
            raise ServiceException('User not found')
    
    def is_email_verified(self, user_id):
        try:
            user = self.get_user_by_id(user_id)
        except RepositoryException as e:
            raise ServiceException('User not found')

        if user.is_verified:
            raise ServiceException('Email already verified')
        
    def update_user(self, user_id, **kwargs):
        try:
            return self.repository.update(user_id, **kwargs)
        except RepositoryException as e:
            raise ServiceException('User update failed')
        
    def get_all_users(self):
        try:
            return self.repository.get_all()
        except RepositoryException as e:
            raise ServiceException('Failed to retrieve users')