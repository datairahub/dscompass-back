from rest_framework_simplejwt.views import TokenObtainPairView

from src.protection_defenders.defenders_auth.rest.serializers.login_serializers import LoginTokenObtainPairSerializer


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer
