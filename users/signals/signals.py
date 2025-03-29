from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from users.models.user import User
from users.models.user_activity_log import UserActivityLog

def get_request_info(request):
    return {
        "ip_address": request.META.get("REMOTE_ADDR"),
        "user_agent": request.META.get("HTTP_USER_AGENT"),
    }

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    info = get_request_info(request)
    UserActivityLog.objects.create(user=user, action="login", **info)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    info = get_request_info(request)
    UserActivityLog.objects.create(user=user, action="logout", **info)

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        UserActivityLog.objects.create(user=instance, action="create", details={"username": instance.username})

@receiver(post_save, sender=User)
def log_user_update(sender, instance, created, **kwargs):
    if not created:
        UserActivityLog.objects.create(user=instance, action="update", details={"username": instance.username})

@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    UserActivityLog.objects.create(user=None, action="delete", details={"username": instance.username})
