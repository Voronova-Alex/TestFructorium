from django.db import models

from apps.account.models import Account
from apps.image.models import Image


class Bookmark(models.Model):
    class UrlTypes(models.TextChoices):
        WEBSITE = "website"
        BOOK = "book"
        ARTICLE = "article"
        MUSIC = "music"
        VIDEO = "video"

    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField()
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="bookmark_images",
        blank=True,
        null=True,
    )
    type_url = models.CharField(choices=UrlTypes.choices)
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}. {self.owner}"

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"
        ordering = ("-id",)
