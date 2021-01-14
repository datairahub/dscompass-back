from django.conf import settings
from rest_framework import serializers

from .form_serializers import FormSerializer
from .question_serializers import QuestionSerializer
from ...models import FormAnswer, Answer, Question


class AnswerFormAnswerSerializer(serializers.ModelSerializer):
    form = FormSerializer()
    created = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    modified = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)

    class Meta:
        model = FormAnswer
        fields = ['id', 'created', 'modified', 'form']


class AnswerSerializer(serializers.ModelSerializer):
    value_u = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    modified = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    question = QuestionSerializer()
    form_answer = AnswerFormAnswerSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'value_u', 'created', 'modified', 'question', 'form_answer']

    def get_value_u(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_superuser:
            admin_cipher = user.init_a
            return admin_cipher.get_value(answer=obj)
        return user.send_signature_to_cipher_and_decrypt_value(value=obj.value_u)


class CreateAnswersSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='value_u', write_only=True)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects, write_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'value']
