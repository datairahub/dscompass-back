from django.contrib.auth.hashers import make_password
from factory import Faker, LazyFunction
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    email = Faker('email')
    password = LazyFunction(lambda: make_password('1Password-strong-strong-very-strong'))

    class Meta:
        model = 'defenders_auth.User'
        django_get_or_create = ('email',)
