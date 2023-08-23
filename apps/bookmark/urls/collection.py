from django.urls import path

from apps.bookmark.views.collection import (
    CollectionCreateView,
    CollectionDetailView,
    CollectionBookmarkListView,
)

urlpatterns = [
    path(
        "collections/",
        CollectionCreateView.as_view(),
        name="collections-create",
    ),
    path(
        "collections/<int:pk>/",
        CollectionDetailView.as_view(),
        name="collections-info",
    ),
    path(
        "collections-bookmarks/",
        CollectionBookmarkListView.as_view(),
        name="collections-bookmarks-info",
    ),
]
