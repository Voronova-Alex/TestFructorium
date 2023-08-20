from django.contrib import admin

from apps.bookmark.models.bookmark import Bookmark
from apps.bookmark.models.collection import Collection


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "type_url",
        "owner",
    )
    list_filter = ("owner",)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
    )
    list_filter = ("owner",)
