from opengraph import opengraph
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bookmark.models.bookmark import Bookmark
from apps.bookmark.utils import get_info
from apps.image.serializers import ImageSerializer


class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = (
            "id",
            "url",
        )

    def validate_url(self, value):
        try:
            opengraph.OpenGraph(url=value)
        except Exception:
            raise ValidationError(f"{value} is invalid for opengraph")
        return value

    def create(self, validated_data):
        validated_data = get_info(validated_data)
        validated_data["owner"] = self.context["request"].user
        print(validated_data)
        return super().create(validated_data)


class BookmarkDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Bookmark
        fields = (
            "id",
            "title",
            "url",
            "type_url",
            "image",
            "description",
            "created",
            "updated",
        )
        extra_kwargs = {
            "updated": {"read_only": True},
            "created": {"read_only": True}
        }



