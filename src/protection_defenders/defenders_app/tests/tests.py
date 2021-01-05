import pytest
from rest_framework.reverse import reverse

from src.protection_defenders.defenders_app.tests.factories import FormAnswerFactory


@pytest.mark.django_db
def test_create_update_and_detail_answers(api_client_with_credentials):
    api_client = api_client_with_credentials[0]
    answers_dict = {'form': 1,
                    'answers':
                        [{"question": 1, "value": "answer text"},
                         {"question": 2, "value": "answer text"}]
                    }
    create_url = reverse('defender_urls:formanswer-list')
    create_response = api_client.post(path=create_url, data=answers_dict, format='json')

    update_url = reverse('defender_urls:formanswer-detail', kwargs={"pk": 1})
    update_response = api_client.patch(path=update_url, data=answers_dict, format='json')

    detail_url = reverse('defender_urls:formanswer-detail', kwargs={"pk": 1})
    detail_response = api_client.get(path=detail_url, format='json')

    assert create_response.status_code == 201
    assert update_response.status_code == 200
    assert detail_response.data['answers'][0]['value_u'] == answers_dict['answers'][0]['value']


@pytest.mark.django_db
def test_list_form_answers(api_client_with_credentials):
    user = api_client_with_credentials[1]
    FormAnswerFactory.create(user=user)

    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:formanswer-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data[0].get('answers') == []


@pytest.mark.django_db
def test_detail_form_answer(api_client_with_credentials):
    user = api_client_with_credentials[1]
    form_answer = FormAnswerFactory.create(user=user)

    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:formanswer-detail', kwargs={"pk": form_answer.pk})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == form_answer.pk


@pytest.mark.django_db
def test_delete_form_answer(api_client_with_credentials):
    user = api_client_with_credentials[1]
    form_answer = FormAnswerFactory.create(user=user)

    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:formanswer-detail', kwargs={"pk": form_answer.pk})
    response = api_client.delete(url)

    assert response.status_code == 204


@pytest.mark.django_db
def test_list_answers(api_client_with_credentials):
    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:answer-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_list_forms(api_client_with_credentials):
    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:form-list')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_form(api_client_with_credentials):
    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:form-detail', kwargs={"pk": 1})
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_languages(api_client_with_credentials):
    api_client = api_client_with_credentials[0]
    url = reverse('defender_urls:language-list')
    response = api_client.get(url)
    assert response.status_code == 200
