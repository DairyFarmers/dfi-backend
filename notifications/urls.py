from django.urls import path
from notifications.views.list_view import NotificationListView

urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notification-list'),
    path('mark-read/', NotificationListView.as_view(), name='notification-mark-read'),
]
