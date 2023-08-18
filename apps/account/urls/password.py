from django.urls import path

from apps.account.views.password import ResetPasswordToken, ResetPassword, ValidateToken

urlpatterns = [
    path(
        "accounts/password-reset/validate-token/",
        ValidateToken.as_view(),
        name="reset-password-validate",
    ),
    path(
        "accounts/password-reset/confirm/",
        ResetPassword.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "accounts/password-reset/",
        ResetPasswordToken.as_view(),
        name="reset-password-request",
    ),
]
