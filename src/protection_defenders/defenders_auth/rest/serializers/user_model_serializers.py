from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.protection_defenders.core.mixins import CheckUserMailMixin

User = get_user_model()


class EmailUserSerializer(CheckUserMailMixin, serializers.ModelSerializer):
    email = serializers.EmailField(required=True, style={'autofocus': True})

    def validate(self, attrs):
        user_valid_email = self.check_login_mail(email=attrs['email'])
        if user_valid_email is None:
            raise ValidationError(_('No active account found with the given credentials'))
        attrs['email'] = user_valid_email
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email',)


class PasswordUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(required=True, style={'input_type': 'password', 'autofocus': True},
                                      write_only=True)
    password2 = serializers.CharField(required=True, style={'input_type': 'password', 'autofocus': True},
                                      write_only=True)

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('The two password fields didn’t match.'))
        try:
            password_validation.validate_password(password=password1, user=self.instance)
        except ValidationError as error:
            raise error

        return data

    class Meta:
        model = User
        fields = ('id', 'password1', 'password2',)
