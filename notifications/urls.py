from django.urls import path
from notifications.views.list_view import NotificationListView
from notifications.views.mark_all_read_view import NotificationMarkAllReadView
from notifications.views.mark_read_view import NotificationMarkReadView
from notifications.views.delete_view import NotificationDeleteView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<str:id>', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('<str:id>/delete', NotificationDeleteView.as_view(), name='notification-delete'),
    path('mark-all/', NotificationMarkAllReadView.as_view(), name='notification-mark-all-read'),
]
