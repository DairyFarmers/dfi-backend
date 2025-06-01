from users.repositories import B2BUserRepository
from django.contrib.auth.hashers import make_password

class B2BUserService:
    def __init__(self):
        self.repository = B2BUserRepository()

    def register_user(self, data: dict):
        # Hash password before saving
        data['password'] = make_password(data['password'])
        return self.repository.create(**data)

    def approve_user(self, user_id: str):
        return self.repository.approve_user(user_id)

    def get_user_details(self, user_id: str):
        return self.repository.get_by_id(user_id)

    def update_credit_limit(self, user_id: str, new_limit: float):
        user = self.repository.get_by_id(user_id)
        if user:
            return self.repository.update(user, credit_limit=new_limit)
        return None