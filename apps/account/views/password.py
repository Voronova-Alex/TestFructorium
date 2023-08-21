import datetime

from django_rest_passwordreset.models import (
    ResetPasswordToken as ResetPasswordTokenModel,
)

from django_rest_passwordreset.serializers import (
    EmailSerializer,
    PasswordTokenSerializer,
)
from django_rest_passwordreset.views import (
    ResetPasswordRequestToken,
    ResetPasswordConfirm,
    ResetPasswordValidateToken,
)
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


@extend_schema(tags=["account | password"])
@extend_schema_view(
    post=extend_schema(
        summary="Создать новый пароль после сброса по email",
        responses={
            "200": OpenApiResponse(
                response=TokenRefreshSerializer,
                description="""
password:

    новый пароль

password_confirmation:

    повторить новый пароль

token:

    токен из параметров запроса

        """,
            ),
        },
    )
)
class ResetPassword(ResetPasswordConfirm):
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        reset_password_token = ResetPasswordTokenModel.objects.filter(key=token).first()
        user = reset_password_token.user

        data = {}
        response = super().post(request, *args, **kwargs)
        token = TokenObtainPairSerializer.get_token(user)
        user.save()
        data["refresh"] = str(token)
        data["access"] = str(token.access_token)
        return Response(data)


@extend_schema(tags=["account | password"])
@extend_schema_view(
    post=extend_schema(
        summary="Восстановить пароль по email ",
        description="""
email:

    email пользователя, куда отправить сообщение для восстановления пароля
        """,
    ),
)
class ResetPasswordToken(ResetPasswordRequestToken):
    serializer_class = EmailSerializer


@extend_schema(tags=["account | password"])
@extend_schema_view(
    post=extend_schema(
        summary="Проверить токен на валидность",
        description="""
token:

    token из query params
        """,
    ),
)
class ValidateToken(ResetPasswordValidateToken):
    pass
