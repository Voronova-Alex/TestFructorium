from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from apps.account.models import Account
from apps.account.serializers.account import (
    AccountDetailSerializer,
    AccountCreateSerializer,
    PasswordUpdateSerializer,
)


@extend_schema(tags=["account"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о текущем пользователе",
    ),
    patch=extend_schema(summary="Обновить данные у текущем пользователе"),
)
class AccountDetailView(RetrieveUpdateAPIView):
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.none()
    http_method_names = ("get", "patch")

    def get_object(self):
        return self.request.user


@extend_schema(tags=["account"])
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация пользователя",
    )
)
class AccountCreateView(CreateAPIView):
    serializer_class = AccountCreateSerializer
    queryset = Account.objects.all()
    permission_classes = ()
    authentication_classes = ()


@extend_schema(tags=["account | password"])
@extend_schema_view(
    patch=extend_schema(
        summary="Изменить пароль",
    ),
)
class PasswordUpdateView(RetrieveUpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    queryset = Account.objects.none()
    http_method_names = ("patch",)

    def get_object(self):
        return self.request.user
