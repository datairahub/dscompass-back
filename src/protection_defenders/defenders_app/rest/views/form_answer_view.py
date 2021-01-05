from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.protection_defenders.core.mixins import GetSerializerActionClassMixin
from ..serializers.form_answer_serializers import FormAnswerSerializer, FormCreateUpdateAnswersSerializer
from ...models import FormAnswer


class FormAnswerViewSet(GetSerializerActionClassMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = FormAnswer.objects.is_active()
    serializer_class = FormAnswerSerializer
    serializer_action_classes = {
        'create': FormCreateUpdateAnswersSerializer,
        'partial_update': FormCreateUpdateAnswersSerializer,
        'list': FormAnswerSerializer,
        'retrieve': FormAnswerSerializer,
        'destroy': FormAnswerSerializer,
    }

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Define queryset levels
        """
        authenticated_user = self.request.user
        if authenticated_user.is_superuser is True:
            return self.queryset
        return FormAnswer.objects.filter(user=authenticated_user)

    # def list(self, *args):
    #     print('-----> eya')
    #     return Response([])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
