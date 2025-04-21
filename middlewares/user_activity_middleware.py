from django.utils.timezone import now
from users.models.user_activity_log import UserActivityLog
import uuid

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            UserActivityLog.objects.create(
                user=request.user,
                action=f"Visited {request.path}",
                timestamp=now(),
                ip_address=request.META.get("REMOTE_ADDR")
            )
        return response