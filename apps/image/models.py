from django.db import models


class Image(models.Model):
    img = models.ImageField(upload_to="images/%Y/%m")
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}. {self.img}"

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ("upload_time",)