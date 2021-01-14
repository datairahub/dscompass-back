from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from ....core.mixins import GetSerializerActionClassMixin
from ....defenders_auth.rest.serializers.user_serializer import RegisterUserSerializer
from ....defenders_auth.rest.serializers.user_model_serializers import EmailUserSerializer


class UserViewSet(GetSerializerActionClassMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = get_user_model().objects
    serializer_class = EmailUserSerializer
    serializer_action_classes = {
        'list': EmailUserSerializer,
        'detail': EmailUserSerializer,
        'create': RegisterUserSerializer,
        'destroy': EmailUserSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated is False:
            return self.queryset.none()
        if user.is_authenticated is True:
            authenticated_user = self.request.user
            return self.queryset.filter(email=authenticated_user.email)
        return self.queryset

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['list', 'create']:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
