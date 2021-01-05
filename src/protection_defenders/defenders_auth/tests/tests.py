import pytest
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse

from src.protection_defenders.defenders_auth.rest.views.login_views import reset_url_token


@pytest.mark.django_db
def test_sign_up(api_client_auth_with_credentials, mailoutbox):
    admin_email = 'admin@mail.com'
    data = {'email': 'user2@mail2.com',
            'password1': '1Password-strong-strong-very-strong',
            'password2': '1Password-strong-strong-very-strong'}

    api_client = api_client_auth_with_credentials[0]
    url = reverse('defender_urls:user-list')
    response = api_client.post(path=url, data=data, format='json')
    mail = mailoutbox[0]

    assert response.status_code == 201
    assert len(mailoutbox) == 1
    assert mail.subject == 'Account activation requested on Defenders app'
    assert mail.from_email == settings.DEFAULT_FROM_EMAIL
    assert list(mail.to) == [admin_email]


@pytest.mark.django_db
def test_activate_account(api_client_auth_with_credentials, create_activation_token):
    user = api_client_auth_with_credentials[1]
    uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = create_activation_token.make_token(user=user)

    api_client = api_client_auth_with_credentials[0]
    url = reverse('login:user-activate-account', kwargs={'uid_b64': uid_b64, 'token': token})
    response = api_client.get(path=url)

    assert response.status_code == 302
    assert response.url == settings.USER_ACTIVATION_REDIRECT_URL


@pytest.mark.django_db
def test_login_sign_in_jwt(api_client_with_out_credentials):
    api_client = api_client_with_out_credentials
    url = reverse('auth_token')
    response = api_client.post(path=url, data={'register_email': 'user@mail.com',
                                               'password': '1Password-strong-strong-very-strong'})

    assert response.status_code == 200
    assert response.data['access'] is not None
    assert response.data['refresh'] is not None


@pytest.mark.django_db
def test_send_reset_email(api_client_auth_with_credentials, mailoutbox):
    admin_email = 'admin@mail.com'
    data = {'email': 'user@mail.com'}

    api_client = api_client_auth_with_credentials[0]
    url = reverse('login:user-send-reset-email')
    response = api_client.post(path=url, data=data, format='json')
    mail = mailoutbox[0]

    assert response.status_code == 200
    assert len(mailoutbox) == 1
    assert mail.subject == 'Reset account on Defenders app'
    assert mail.from_email == settings.DEFAULT_FROM_EMAIL
    assert list(mail.to) == [admin_email]


@pytest.mark.django_db
def test_reset_token(api_client_auth_with_credentials, create_reset_token):
    user = api_client_auth_with_credentials[1]
    uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = create_reset_token.make_token(user=user)

    api_client = api_client_auth_with_credentials[0]
    url = reverse('login:user-check-token-and-reset-passwd', kwargs={'uid_b64': uid_b64,
                                                                     'token': token})
    response = api_client.get(path=url)

    assert response.status_code == 302
    assert response.url == f"/login/reset_password/{uid_b64}/{reset_url_token}/"


@pytest.mark.django_db
def test_list_users(api_client_auth_with_credentials):
    api_client = api_client_auth_with_credentials[0]
    url = reverse('defender_urls:user-list')
    response = api_client.get(path=url)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_detail(api_client_auth_with_credentials):
    api_client = api_client_auth_with_credentials[0]
    user = api_client_auth_with_credentials[1]
    url = reverse('defender_urls:user-detail', kwargs={'pk': user.id})
    response = api_client.get(path=url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_delete(api_client_auth_with_credentials):
    api_client = api_client_auth_with_credentials[0]
    user = api_client_auth_with_credentials[1]
    url = reverse('defender_urls:user-detail', kwargs={'pk': user.id})
    response = api_client.delete(path=url)

    assert response.status_code == 204
