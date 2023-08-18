from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
    )
    fieldsets = (
        (
            "Системная информация",
            {
                "fields": (
                    "password",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    # "is_deleted",
                    # "date_joined",
                    "email",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("password1", "password2"),
            },
        ),
    )
    ordering = ("-email",)


