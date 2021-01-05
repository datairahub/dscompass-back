import pytest

from src.protection_defenders.defenders_app.tests.factories import LanguageFactory, FormFactory, BlockFactory, \
    QuestionFactory
from src.protection_defenders.defenders_auth.tests.factories import UserFactory


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        UserFactory.create(email='user@mail.com')
        UserFactory.create(is_superuser=True, email='admin@mail.com')
        language = LanguageFactory.create()
        form = FormFactory.create(language=language)
        block = BlockFactory.create()
        QuestionFactory.create_batch(2, form=form, block=block)


@pytest.fixture()
def create_user(db):
    def make_user(**kwargs):
        return UserFactory.create(**kwargs)

    return make_user


@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    from rest_framework_simplejwt.tokens import RefreshToken
    user = create_user(email='user@mail.com')
    refresh = RefreshToken.for_user(user)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.force_authenticate(user=user)
    yield api_client, user
    api_client.force_authenticate(user=None)
