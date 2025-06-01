from users.repositories import BaseRepository
from users.models import B2BUser
from django.utils import timezone

class B2BUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(B2BUser)

    def approve_user(self, user_id: str) -> B2BUser:
        user = self.get_by_id(user_id)
        if user:
            return self.update(
                user,
                is_approved=True,
                approval_date=timezone.now()
            )
        return None

    def get_pending_approvals(self):
        return self.filter(is_approved=False)

    def get_by_tax_id(self, tax_id: str) -> B2BUser:
        return self.model.objects.filter(tax_id=tax_id).first()