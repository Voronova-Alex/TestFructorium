from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

from apps.bookmark.models.collection import Collection
from apps.bookmark.serializers.bookmark import BookmarkDetailSerializer
from apps.bookmark.serializers.collection import (
    CollectionDetailSerializer,
    CollectionUpdateSerializer,
    CollectionCreateSerializer,
)


@extend_schema(tags=["collection"])
@extend_schema_view(
    get=extend_schema(
        summary="Посмотреть информацию о коллекции",
    ),
    patch=extend_schema(
        summary="Редактировать коллекцию",
        description="""
        Чтобы добавить статью в коллекцию необходимо передать список статей,
        которые есть в коллекции + объект, который добавляем.
        Чтобы удалить статью из коллекции, необходимо передать список статье без объекта,
        который удаляем
        """,
    ),
    delete=extend_schema(
        summary="Удалить коллекцию",
    ),
)
class CollectionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkDetailSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Collection.objects.none()
        return Collection.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CollectionDetailSerializer
        return CollectionUpdateSerializer


@extend_schema(tags=["collection"])
@extend_schema_view(
    post=extend_schema(
        summary="Создать коллекцию",
    )
)
class CollectionCreateView(CreateAPIView):
    serializer_class = CollectionCreateSerializer
    queryset = Collection.objects.all()
