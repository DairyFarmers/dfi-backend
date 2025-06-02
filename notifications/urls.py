from django.urls import path
from notifications.views.list_view import NotificationListView
from notifications.views.mark_all_read_view import NotificationMarkAllReadView
from notifications.views.mark_read_view import NotificationMarkReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:id>', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('mark-all', NotificationMarkAllReadView.as_view(), name='notification-mark-all-read'),
]
