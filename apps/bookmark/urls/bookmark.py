from django.urls import path

from apps.bookmark.views.bookmark import BookmarkDetailView, BookmarkCreateView

urlpatterns = [
    path(
        "bookmarks/",
        BookmarkCreateView.as_view(),
        name="bookmark-create",
    ),
    path(
        "bookmarks/<int:pk>/",
        BookmarkDetailView.as_view(),
        name="bookmark-info",
    ),
]
