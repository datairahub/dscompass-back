from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from .answer_serializers import AnswerSerializer, CreateAnswersSerializer
from .form_serializers import FormSerializer
from ...models import FormAnswer, Answer, Form


class FormAnswerSerializer(serializers.ModelSerializer):
    form = FormSerializer()
    created = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    modified = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    answers = AnswerSerializer(source='f_answer_related', many=True)

    class Meta:
        model = FormAnswer
        fields = ['id', 'form', 'name', 'created', 'modified', 'answers']


class FormCreateUpdateAnswersSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(queryset=Form.objects, write_only=True)
    answers = CreateAnswersSerializer(source='f_answer_related', many=True, write_only=True)

    class Meta:
        model = FormAnswer
        fields = ['id', 'form', 'answers', 'name']

    def create(self, validated_data):
        answers = validated_data.pop('f_answer_related', [])
        instance, created = FormAnswer.objects.get_or_create(**validated_data)
        if not created:
            Answer.objects.filter(form_answer=instance).delete()
        request = self.context.get('request')
        user = request.user
        for answer in answers:
            value = answer.pop('value_u', None)
            value_u = user.crypt_and_verify_from_cipher(value=value)
            value_a = user.init_a.crypt_and_verify_from_cipher(value=value)
            Answer.objects.create(form_answer=instance, value_u=value_u, value_a=value_a, **answer)
        return instance

    def update(self, instance, validated_data):
        instance.modified = timezone.now()
        instance.name = validated_data.get('name', '')
        answers_data = validated_data.get('f_answer_related', [])
        instance.modified = timezone.now()

        request = self.context.get('request')
        user = request.user
        for answer in answers_data:
            answer_db, created = Answer.objects.get_or_create(question=answer['question'],
                                                              form_answer_id=instance.pk)
            answer_db.value_u = user.crypt_and_verify_from_cipher(value=answer['value_u'])
            answer_db.value_a = user.init_a.crypt_and_verify_from_cipher(value=answer['value_u'])
            answer_db.save()
        instance.save()
        return instance
