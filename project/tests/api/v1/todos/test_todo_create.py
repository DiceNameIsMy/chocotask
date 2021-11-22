import pytest

from rest_framework.test import APIClient

from django.urls import reverse

from apps.accounts.models import UserType

TODOS_LIST_URL = reverse('todos-list')

DEFAULT_TODO_VALUES = {'title': 'test', 'description': 'test'}


def create_todo(api_client: APIClient, data: dict = {}):
    return api_client.post(
        TODOS_LIST_URL,
        DEFAULT_TODO_VALUES | data
    )


@pytest.mark.django_db
def test_create_todo_as_employee(api_client: APIClient, authenticate, user_employee):
    authenticate(api_client, user_employee)
    response = create_todo(api_client)

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_todo_as_guest(api_client: APIClient, authenticate, user_guest):
    authenticate(api_client, user_guest)
    response = create_todo(api_client)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_todo_without_credentials(api_client: APIClient):
    response = create_todo(api_client)

    assert response.status_code == 401
