import pytest
from django.contrib.auth.tokens import default_token_generator

from src.protection_defenders.defenders_auth.tests.factories import UserFactory
from src.protection_defenders.defenders_auth.tokens import account_activation_token


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        UserFactory.create(email='user@mail.com', password="1Password-strong-strong-very-strong")
        UserFactory.create(is_superuser=True, email='admin@mail.com', password="1Password-strong-strong-very-strong")


@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture()
def create_reset_token():
    return default_token_generator


@pytest.fixture()
def create_activation_token():
    return account_activation_token


@pytest.fixture()
def create_auth_user(db):
    def make_auth_user(**kwargs):
        return UserFactory.create(**kwargs)

    return make_auth_user


@pytest.fixture
def api_client_auth_with_credentials(db, create_auth_user, api_client):
    from rest_framework_simplejwt.tokens import RefreshToken
    user = create_auth_user(email='user_auth@mail.com', password="1Password-strong-strong-very-strong")

    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.force_authenticate(user=user)
    yield api_client, user
    api_client.force_authenticate(user=None)


@pytest.fixture
def api_client_with_out_credentials(api_client):
    api_client.force_authenticate(user=None)
    yield api_client

