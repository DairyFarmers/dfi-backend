# users URL Configuration

from django.contrib import admin
from django.urls import path
from users.views.signup_view import SignupView
from users.views.login_view import LoginView

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
]
