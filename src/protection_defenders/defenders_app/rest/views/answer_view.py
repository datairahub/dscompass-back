from rest_framework import mixins, viewsets

from ..serializers.answer_serializers import AnswerSerializer
from ...models import Answer


class AnswerViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Answer.objects
    serializer_class = AnswerSerializer

    def get_queryset(self):
        authenticated_user = self.request.user
        if authenticated_user.is_superuser is True:
            self.queryset.all()
        return self.queryset.user_owner(user=authenticated_user)
