from django.urls import path

from apps.image.views import ImageCreateView, ImageDeleteView

urlpatterns = [
    path("images/", ImageCreateView.as_view(), name="image-create"),
    path("images/<int:pk>/", ImageDeleteView.as_view(), name="image-delete"),
]
