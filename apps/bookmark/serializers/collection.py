from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.bookmark.models.bookmark import Bookmark
from apps.bookmark.models.collection import Collection
from apps.bookmark.serializers.bookmark import BookmarkDetailSerializer


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            "id",
            "title",
            "description",
        )

    @transaction.atomic
    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class CollectionDetailSerializer(serializers.ModelSerializer):
    links = BookmarkDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = (
            "id",
            "title",
            "description",
            "links",
            "created",
            "updated",
        )
        extra_kwargs = {"updated": {"read_only": True}, "created": {"read_only": True}}


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get("request", None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(owner=self.context["request"].user)


class CollectionUpdateSerializer(serializers.ModelSerializer):
    links = UserFilteredPrimaryKeyRelatedField(
        queryset=Bookmark.objects.all(), many=True
    )

    class Meta:
        model = Collection
        fields = (
            "title",
            "description",
            "links",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        links = []
        if "links" in validated_data:
            links = validated_data["links"]
            validated_data.pop("links")
        obj = super().update(instance, validated_data)
        if links:
            instance.links.set(links)
        return obj


class CollectionBookmarkSerializer(serializers.Serializer):
    collections = serializers.SerializerMethodField()
    none = serializers.SerializerMethodField()

    @extend_schema_field(CollectionDetailSerializer(many=True))
    def get_collections(self, instance):
        context = {"request": self.context["request"]}
        queryset = Collection.objects.filter(
            owner=self.context["request"].user
        ).order_by("title")
        return CollectionDetailSerializer(queryset, many=True, context=context).data

    @extend_schema_field(BookmarkDetailSerializer(many=True))
    def get_none(self, instance):
        context = {"request": self.context["request"]}
        queryset = Bookmark.objects.filter(
            owner=self.context["request"].user, collections__isnull=True
        ).order_by("title")
        return BookmarkDetailSerializer(queryset, many=True, context=context).data
