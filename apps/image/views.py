from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.image.models import Image
from apps.image.serializers import ImageSerializer


@extend_schema(tags=["media | image"])
@extend_schema_view(
    post=extend_schema(
        summary="Создать фотографию",
    ),
)
class ImageCreateView(CreateAPIView):
    permission_classes = (JWTAuthentication,)
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser]
    queryset = Image.objects.all()


@extend_schema(tags=["media | image"])
@extend_schema_view(
    delete=extend_schema(
        summary="Удалить фотографию",
    ),
)
class ImageDeleteView(DestroyAPIView):
    permission_classes = (JWTAuthentication,)
    serializer_class = ImageSerializer
    queryset = Image.objects.all()