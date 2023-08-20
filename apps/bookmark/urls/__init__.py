from .bookmark import urlpatterns as bookmark_urlpatterns
from .collection import urlpatterns as collection_urlpatterns

app_name = "bookmark"

urlpatterns = bookmark_urlpatterns + collection_urlpatterns

__all__ = ["urlpatterns"]
