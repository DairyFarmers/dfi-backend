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
from users.views.user_list_view import UserListView
from users.views.user_view import UserView
from users.views.user_activity_logs_view import UserActivityLogsView
from users.views.user_role_view import UserRoleView
from users.views.user_role_detail_view import UserRoleDetailView
from users.views.initialize_default_roles_view import InitializeDefaultRolesView
from users.utils.permissions import get_user_permissions, get_all_permissions
from users.views.b2b_registration_view import B2BRegistrationView
from users.views.b2b_approval_view import B2BApprovalView
from users.views.settings_view import UserSettingsView
from users.views.user_contact_view import UserContactView
from users.views.user_location_view import UserLocationView
from users.views.change_password_view import ChangePasswordView
from users.views.logout_view import LogoutView
from users.views.user_detail_view import UserDetailView

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('login', LoginView.as_view(), name='login'),
    path('token/verification', TokenVerificationView.as_view(), name='token_verification'),
    path('verify-email', EmailVerificationView.as_view(), name='verification'),
    path('send-otp', PasscodeView.as_view(), name='passcode'),
    path('password-reset-request', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset', PasswordResetView.as_view(), name='password_reset'),
    path('list', UserListView.as_view(), name='user-list'),
    path('detail', UserView.as_view(), name='user-detail'),
    path("activity-logs", UserActivityLogsView.as_view(), name="user-activity-logs"),
    path('roles/', UserRoleView.as_view(), name='role-list'),
    path('roles/<uuid:role_id>/', UserRoleDetailView.as_view(), name='role-detail'),
    path('roles/initialize/', InitializeDefaultRolesView.as_view(), name='initialize-roles'),
    path('permissions/', get_user_permissions, name='user-permissions'),
    path('permissions/all', get_all_permissions, name='all-permissions'),
    path('b2b/register/', B2BRegistrationView.as_view(), name='b2b-register'),
    path('b2b/<uuid:user_id>/approve/', B2BApprovalView.as_view(), name='b2b-approve'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('contact/', UserContactView.as_view(), name='user-contact'),
    path('locations/', UserLocationView.as_view(), name='user-locations'),
    path('locations/<uuid:location_id>', UserLocationView.as_view(), name='delete-location'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('<uuid:user_id>/', UserDetailView.as_view(), name='user-detail-view'),
]
