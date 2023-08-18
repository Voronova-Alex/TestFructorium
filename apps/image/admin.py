from django.contrib import admin

from apps.image.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "img", "upload_time")
