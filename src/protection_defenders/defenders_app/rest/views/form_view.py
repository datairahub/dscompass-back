from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers.form_serializers import FormSerializer
from ...models import Form


class FormViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Form.objects.is_active()
    serializer_class = FormSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Define queryset levels
        """
        language = self.request.query_params.get('language', None)

        return Form.objects.filter(is_active=True, language__code=language) \
            if language \
            else Form.objects.filter(is_active=True)
