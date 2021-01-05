from rest_framework import serializers

from .question_serializers import QuestionSerializer
from ...models import Form


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(source='question_related', many=True)

    class Meta:
        model = Form
        fields = ['id', 'questions_length', 'name', 'display_name',
                  'questions', 'language', 'introduction', 'conclusion',
                  'created']
