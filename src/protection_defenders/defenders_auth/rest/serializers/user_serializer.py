from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.protection_defenders.defenders_auth.rest.serializers.user_model_serializers import PasswordUserSerializer
from src.protection_defenders.defenders_auth.tokens import account_activation_token


class RegisterUserSerializer(PasswordUserSerializer):
    email = serializers.EmailField(required=True, style={'autofocus': True})

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password1')
        request = self.context['request']
        try:
            user = get_user_model().objects.create_user(register_email=email, password=password, is_active=False)
            subject_template_name = 'defenders_auth/activate_account/subject.txt'
            email_template_name = 'defenders_auth/activate_account/body.html'
            user.send_token_email(uri=request.build_absolute_uri('/login/activate/'),
                                  subject_template_name=subject_template_name,
                                  email_template_name=email_template_name,
                                  generator_token=account_activation_token)
        except IntegrityError:
            raise ValidationError(_('User has already been registered'))
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password1', 'password2',)
