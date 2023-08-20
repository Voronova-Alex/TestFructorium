from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.account.models import Account
from apps.image.serializers import ImageSerializer
from link.exceptions.account import (
    EmailAccountException,
    WrongOldPasswordException,
)


class AccountDetailSerializer(serializers.ModelSerializer):
    photo_read = ImageSerializer(source="photo", read_only=True)

    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "email",
            "photo",
            "photo_read",
        )
        extra_kwargs = {"photo": {"write_only": True}}

    def validate_email(self, value):
        if Account.objects.filter(email=value):
            raise EmailAccountException

        return value


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetailSerializer.Meta.model
        fields = (
            "password",
            *AccountDetailSerializer.Meta.fields,
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate_email(self, value):
        if Account.objects.filter(email=value):
            raise EmailAccountException

        return value

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class PasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ("password", "old_password")

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise WrongOldPasswordException
        return value

    def validate(self, attrs):
        for value in self.fields.keys():
            if not attrs.get(value, None):
                raise serializers.ValidationError({value: "this field is required"})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
