# users URL Configuration

from django.contrib import admin
from django.urls import path
from users.views.registration_view import RegistrationView
from users.views.login_view import LoginView
from users.views.token_verification_view import TokenVerificationView
from users.views.email_verification_view import EmailVerificationView
from users.views.passcode_view import PasscodeView
from users.views.password_reset_request_view import PasswordResetRequestView
from users.views.password_reset_view import PasswordResetView
from users.views.users_list_view import UserListView

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('login', LoginView.as_view(), name='login'),
    path('token/verification', TokenVerificationView.as_view(), name='token_verification'),
    path('verification', EmailVerificationView.as_view(), name='verification'),
    path('otp', PasscodeView.as_view(), name='passcode'),
    path('password-reset-request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset', PasswordResetView.as_view(), name='password_reset'),
    path('list', UserListView.as_view(), name='user-list'),
]
