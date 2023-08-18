from django.urls import path

from apps.account.views.authentication import TokenView, AuthenticationView

urlpatterns = [
    path(
        "accounts/auth/",
        AuthenticationView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "accounts/auth/refresh/",
        TokenView.as_view(),
        name="token-refresh",
    ),
]
