# users URL Configuration

from django.contrib import admin
from django.urls import path
from users.views.signup_view import SignupView
from users.views.login_view import LoginView
from users.views.token_verification_view import TokenVerificationView

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('token/verification', TokenVerificationView.as_view(), name='token_verification'),
]
