from django.conf import settings
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.admin import sensitive_post_parameters_m
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.login_serializers import ActivateUserSerializer, ResetPasswordSerializer
from ..serializers.user_model_serializers import EmailUserSerializer
from ...tokens import account_activation_token

internal_reset_session_token = '_passwd_reset_token'
reset_url_token = 'set-passwd'
user_model = get_user_model()


class LoginViewSet(viewsets.GenericViewSet):
    queryset = user_model.objects.none()
    serializer_class = EmailUserSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginViewSet, self).dispatch(*args, **kwargs)

    @staticmethod
    def get_user(uid_b64):
        try:
            uid = urlsafe_base64_decode(uid_b64).decode()
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist, ValidationError):
            user = None
        return user

    @action(methods=['get'], detail=False, serializer_class=ActivateUserSerializer,
            url_path=r'activate/(?P<uid_b64>[^/.]+)/(?P<token>[^/.]+)')
    def activate_account(self, request, uid_b64, token):
        user = self.get_user(uid_b64)

        if user is not None and account_activation_token.check_token(user=user, token=token) is True:
            user.is_active = True
            user.save()

            subject_template_name = 'defenders_auth/activate_notification/subject.txt'
            email_template_name = 'defenders_auth/activate_notification/body.html'
            user.send_activation_notification(subject_template_name=subject_template_name,
                                              email_template_name=email_template_name)

            return HttpResponseRedirect(redirect_to=settings.USER_ACTIVATION_REDIRECT_URL)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, serializer_class=EmailUserSerializer,
            url_path=r'reset_password')
    def send_reset_email(self, request):
        serializer = EmailUserSerializer(data=request.data)

        if serializer.is_valid():
            user = get_user_model().objects.get(email=serializer.data['email'])

            subject_template_name = 'defenders_auth/reset_password/subject.txt'
            email_template_name = 'defenders_auth/reset_password/body.html'
            user.send_token_email(uri=request.build_absolute_uri('/login/reset_password/'),
                                  subject_template_name=subject_template_name,
                                  email_template_name=email_template_name,
                                  generator_token=default_token_generator)
            user.save()

            return Response({'status': 'email sent'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'post'], detail=False,
            serializer_class=ResetPasswordSerializer,
            url_path=r'reset_password/(?P<uid_b64>[^/.]+)/(?P<token>[^/.]+)')
    def check_token_and_reset_passwd(self, request, uid_b64, token):
        user = self.get_user(uid_b64)
        if user is not None:
            if token == reset_url_token:
                session_token = request.session.get(internal_reset_session_token)
                token_is_valid = default_token_generator.check_token(user, session_token)
                if token_is_valid is True and request.method == 'POST':
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(user=user)
                    update_session_auth_hash(request=request, user=user)
                    return Response({'status': 'password set'})
            else:
                token_is_valid = default_token_generator.check_token(user, token)
                if token_is_valid and request.method == 'GET':
                    # Store the token in the session and redirect to the
                    # password reset action at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    request.session[internal_reset_session_token] = token
                    reset_password_url = self.request.path.replace(token, reset_url_token)
                    return HttpResponseRedirect(reset_password_url)
        return Response(status=status.HTTP_404_NOT_FOUND)
