from .account import urlpatterns as account_urlpatterns
from .password import urlpatterns as password_urlpatterns
from .authentication import urlpatterns as auth_urlpatterns

app_name = "account"

urlpatterns = account_urlpatterns + password_urlpatterns + auth_urlpatterns

__all__ = ["urlpatterns"]
