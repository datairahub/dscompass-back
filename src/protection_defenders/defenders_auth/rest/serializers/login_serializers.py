from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from src.protection_defenders.core.mixins import CheckUserMailMixin
from src.protection_defenders.defenders_auth.rest.serializers.user_model_serializers import PasswordUserSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainSerializer):

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs and 'email' in kwargs['data']:
            kwargs['data']['register_email'] = kwargs['data']['email']
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        self.user = authenticate(None, username=attrs['register_email'], password=attrs['password'])

        if not self.user:
            return {}

        refresh = self.get_token(self.user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class ActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active',)


class ResetPasswordSerializer(PasswordUserSerializer):
    def save(self, user):
        user.set_password(self.validated_data.get('password1'))
        user.save()

    class Meta:
        model = User
        fields = ('id', 'password1', 'password2',)


class LoginTokenObtainSerializer(CheckUserMailMixin, serializers.Serializer):
    username_field = get_user_model().EMAIL_FIELD
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        user_valid_email = self.check_login_mail(email=attrs[self.username_field])
        if user_valid_email is not None:
            authenticate_kwargs['username'] = user_valid_email

        self.user = authenticate(**authenticate_kwargs)
        if self.user is None or self.user.is_active is False:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class LoginTokenObtainPairSerializer(LoginTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
