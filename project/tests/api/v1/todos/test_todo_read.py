import pytest

from rest_framework.test import APIClient

from django.urls import reverse

from apps.accounts.models import UserType

TODOS_LIST_URL = reverse('todos-list')

DEFAULT_TODO_VALUES = {'title': 'test', 'description': 'test'}


def get_todo(api_client: APIClient):
    return api_client.get(TODOS_LIST_URL)


def get_todo_detail(api_client: APIClient, pk: int):
    return api_client.get(f'{TODOS_LIST_URL}{pk}/')


@pytest.mark.django_db
def test_get_todos_list(api_client: APIClient, authenticate, user_guest, user_employee):
    # not authorized
    response = get_todo(api_client)
    assert response.status_code == 401

    # authorized as guest
    authenticate(api_client, user_guest)
    response = get_todo(api_client)
    assert response.status_code == 200

    # authorized as employee
    authenticate(api_client, user_employee)
    response = get_todo(api_client)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_todo_detail(api_client: APIClient, authenticate, user_guest, user_employee, user_employee_and_todo):
    user_author, todo = user_employee_and_todo

    # accessing without creds
    response = get_todo_detail(api_client, todo.pk)
    assert response.status_code == 401

    # accessing as author
    authenticate(api_client, user_author)
    response = get_todo_detail(api_client, todo.pk)
    assert response.status_code == 200

    # accessing as another employee
    authenticate(api_client, user_employee)
    response = get_todo_detail(api_client, todo.pk)
    assert response.status_code == 200

    # accesing as guest
    authenticate(api_client, user_guest)
    response = get_todo_detail(api_client, todo.pk)
    assert response.status_code == 200




