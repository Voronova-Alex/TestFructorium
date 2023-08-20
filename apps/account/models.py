from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from apps.account.managers import AccountManager
from apps.account.utils import send_email_user
from apps.image.models import Image
from link.settings import SERVER_NAME, URL_RESET_PASSWORD


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    photo = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="account_images", blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    USERNAME_FIELD = "email"

    objects = AccountManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    email_plaintext_message = (
        f"{SERVER_NAME}{URL_RESET_PASSWORD}{reset_password_token.key}/"
    )
    subject = "Password generation token for Base"
    email = reset_password_token.user.email
    #тут можно использовать celery

    send_email_user.delay(subject, email_plaintext_message, email)
