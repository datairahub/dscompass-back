from django.conf import settings
from rest_framework import serializers

from ...models import Block, Question, QuestionFile


class QuestionBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'name', 'display_name', 'color', 'order']


class QuestionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionFile
        fields = ['id', 'name', 'file']


class QuestionSerializer(serializers.ModelSerializer):
    block = QuestionBlockSerializer()
    created = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    modified = serializers.DateTimeField(format=settings.DEFAULT_DATE_TIME_FORMAT)
    files = QuestionFileSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'order', 'block', 'form', 'question', 'context', 'example',
                  'more_info', 'default_response', 'related_question', 'image',
                  'files', 'created', 'modified']
