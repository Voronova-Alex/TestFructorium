import os
import jwt

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.account.models import Account


@extend_schema(tags=["account | authentication"])
@extend_schema_view(
    post=extend_schema(
        summary="Аутентифицировать пользователя",
        description="""
        Принимает набор учетных данных пользователя и возвращает пару веб-токенов доступа
        """,
    ),
)
class AuthenticationView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        user = Account.objects.get(email=request.data["email"])
        user.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(tags=["account | authentication"])
@extend_schema_view(
    post=extend_schema(
        summary="Обновить токен",
        description="""
        Принимает refresh токен и возвращает пару веб-токенов доступа, если refresh действителен""",
    ),
)
class TokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = jwt.decode(
            str(request.data["refresh"]),
            str(os.environ.get("SECRET_KEY")),
            algorithms=["HS256"],
        )
        account = Account.objects.get(id=user["user_id"])
        account.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
