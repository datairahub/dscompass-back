from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt import serializers, exceptions, views

from src.protection_defenders.core.mixins import CheckUserMailMixin
from src.protection_defenders.defenders_auth.rest.serializers.login_serializers import MyTokenObtainPairSerializer

class CookieTokenViewBase(views.TokenViewBase, CheckUserMailMixin):
    """
    Cookie JWT Token View
    - If refresh token is present (added on CookieJWTMiddleware)
      add it to request data
    - If response is going to return the refresh token,
      remove it from the data and set is as a HttpOnly cookie

    Custom implementation of Django Simple JWT
    https://github.com/SimpleJWT/django-rest-framework-simplejwt/blob/073d83ccbaa2e6956dde27db6bd258ad8ea2d8ea/rest_framework_simplejwt/views.py#L9
    """

    def post(self, request, *args, **kwargs):
        if hasattr(request, 'data') and request.data.get('email'):
            # Check if the user is register
            user_email = self.check_login_mail(request.data['email'])
            request.data.update({"email": user_email})
        elif hasattr(request, 'refresh'):
            # Add refresh token to data if present
            request.data.update({"refresh": request.refresh})

        serializer = MyTokenObtainPairSerializer(data=request.data)

        if not serializer.is_valid():
            raise exceptions.InvalidToken('Invalid Token')

        # Remove refresh token from response data
        refresh_cookie = serializer.validated_data.pop('refresh', None)

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        if refresh_cookie:
            # Add refresh token to cookie with HttpOnly, Secure and other flags
            response.set_cookie(
                key=settings.SIMPLE_JWT['COOKIE_REFRESH_KEY'],
                value=refresh_cookie,
                expires=datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['COOKIE_HTTPONLY'],
                domain=settings.SIMPLE_JWT['COOKIE_DOMAIN'],
                samesite=settings.SIMPLE_JWT['COOKIE_SAMESITE'],
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            )

        return response


class TokenObtainPairView(CookieTokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    https://github.com/SimpleJWT/django-rest-framework-simplejwt/blob/master/rest_framework_simplejwt/views.py
    """
    serializer_class = serializers.TokenObtainPairSerializer


class TokenRefreshView(CookieTokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    https://github.com/SimpleJWT/django-rest-framework-simplejwt/blob/master/rest_framework_simplejwt/views.py
    """
    serializer_class = serializers.TokenRefreshSerializer


@api_view(['POST'])
def TokenLogoutView(request):
    """
    Logouts the user and removes the refresh token cookie
    """
    response = JsonResponse({})
    response.delete_cookie(settings.SIMPLE_JWT['COOKIE_REFRESH_KEY'])
    return response
