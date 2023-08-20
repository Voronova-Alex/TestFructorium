from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    ListCreateAPIView,
)

from apps.bookmark.models.bookmark import Bookmark
from apps.bookmark.serializers.bookmark import (
    BookmarkDetailSerializer,
    BookmarkCreateSerializer,
)


@extend_schema(tags=["bookmark"])
@extend_schema_view(
    get=extend_schema(
        summary="Посмотреть информацию о закладке",
    ),
    delete=extend_schema(
        summary="Удалить закладку",
    ),
)
class BookmarkDetailView(RetrieveDestroyAPIView):
    serializer_class = BookmarkDetailSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Bookmark.objects.none()

        return Bookmark.objects.filter(owner=self.request.user)


@extend_schema(tags=["bookmark"])
@extend_schema_view(
    post=extend_schema(
        summary="Создать закладку",
    )
)
class BookmarkCreateView(ListCreateAPIView):
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Bookmark.objects.none()

        return Bookmark.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookmarkDetailSerializer
        return BookmarkCreateSerializer
