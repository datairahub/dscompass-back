from rest_framework import serializers

from ...models import Language


class LanguageSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    @staticmethod
    def get_file(obj):
        return obj.file.url

    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'file']
