from factory import SubFactory, Faker
from factory.django import DjangoModelFactory, FileField, ImageField

from src.protection_defenders.defenders_auth.tests.factories import UserFactory


class LanguageFactory(DjangoModelFactory):
    name = Faker('word')
    code = Faker('pystr', max_chars=2)
    file = FileField()

    class Meta:
        model = 'defenders_app.Language'
        django_get_or_create = ('name', 'code',)


class FormFactory(DjangoModelFactory):
    name = Faker('word')
    display_name = Faker('word')
    introduction = Faker('text')
    conclusion = Faker('text')
    language = SubFactory(LanguageFactory)

    class Meta:
        model = 'defenders_app.Form'
        django_get_or_create = ('name', 'display_name',)


class BlockFactory(DjangoModelFactory):
    name = Faker('word')
    display_name = Faker('word')
    color = Faker('color')
    order = Faker('pyint')

    class Meta:
        model = 'defenders_app.Block'
        django_get_or_create = ('name',)


class QuestionFactory(DjangoModelFactory):
    order = Faker('pyint')
    block = SubFactory(BlockFactory)
    form = SubFactory(FormFactory)
    question = Faker('text')
    image = ImageField()
    default_response = Faker('text')
    context = Faker('text')
    example = Faker('text')
    more_info = Faker('text')

    class Meta:
        model = 'defenders_app.Question'
        django_get_or_create = ('question',)


class QuestionFileFactory(DjangoModelFactory):
    file = FileField()
    name = Faker('sentence')
    description = Faker('text')
    question = SubFactory(QuestionFactory)

    class Meta:
        model = 'defenders_app.QuestionFile'
        django_get_or_create = ('name',)


class FormAnswerFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    form = SubFactory(FormFactory)
    name = Faker('word')

    class Meta:
        model = 'defenders_app.FormAnswer'


class AnswerFactory(DjangoModelFactory):
    question = SubFactory(QuestionFactory)
    form_answer = SubFactory(FormAnswerFactory)
    value_u = Faker('text')
    value_a = Faker('text')

    class Meta:
        model = 'defenders_app.Answer'
        django_get_or_create = ('question',)
