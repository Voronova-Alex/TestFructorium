from django.db import models

from apps.account.models import Account
from apps.bookmark.models.bookmark import Bookmark


class Collection(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    links = models.ManyToManyField(Bookmark, blank=True, related_name="collections")
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="collections"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}. {self.owner}"

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        ordering = ("-id",)
