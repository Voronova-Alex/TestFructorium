from django.contrib.auth.base_user import BaseUserManager


class AccountManager(BaseUserManager):
    """Менеджер модели Account"""

    def create_user(self, email, password=None, **extra_fields):
        """Создание пользователя"""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError("The email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def get_queryset(self):
        """Получить данные всех аккаунтов"""

        return BaseUserManager.get_queryset(self)
