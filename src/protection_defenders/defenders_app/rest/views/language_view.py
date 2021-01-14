from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from ..serializers.language_serializers import LanguageSerializer
from ...models import Language


class LanguageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Language.objects
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny,)
