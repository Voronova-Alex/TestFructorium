from django.urls import path

from apps.account.views.account import (
    AccountCreateView,
    AccountDetailView,
    PasswordUpdateView,
)

urlpatterns = [
    path(
        "accounts/",
        AccountCreateView.as_view(),
        name="account-create",
    ),
    path(
        "accounts/info/",
        AccountDetailView.as_view(),
        name="account-info",
    ),
    path(
        "accounts/password/",
        PasswordUpdateView.as_view(),
        name="password-update",
    ),
]
