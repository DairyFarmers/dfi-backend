from django.urls import path
from notifications.views.list_view import NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:id>/read', NotificationListView.as_view(), name='notification-mark-read'),
]
