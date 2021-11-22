import pytest

from rest_framework.test import APIClient

from django.urls import reverse


TODOS_LIST_URL = reverse('todos-list')
DEFAULT_UPDATE_TODO_VALUES = {
    'title': 'new_test',
    'description': 'new_description'
}

def patch_todo(api_client: APIClient, pk: int):
    return api_client.patch(
        f'{TODOS_LIST_URL}{pk}/',
        DEFAULT_UPDATE_TODO_VALUES
    )

def put_todo(api_client: APIClient, pk: int):
    return api_client.put(
        f'{TODOS_LIST_URL}{pk}/',
        DEFAULT_UPDATE_TODO_VALUES
    )

def delete_todo(api_client: APIClient, pk: int):
    return api_client.delete(
        f'{TODOS_LIST_URL}{pk}/',
    )


@pytest.mark.django_db
@pytest.mark.parametrize('action, expected_code', [(put_todo, 401), (patch_todo, 401), (delete_todo, 401)])
def test_not_authenticated(api_client: APIClient, user_employee_and_todo, action, expected_code):
    user_author, todo = user_employee_and_todo

    response = action(api_client, todo.pk)
    assert response.status_code == expected_code


@pytest.mark.django_db
@pytest.mark.parametrize('action, expected_code', [(put_todo, 403), (patch_todo, 403), (delete_todo, 403)])
def test_guest(api_client: APIClient, authenticate, user_employee_and_todo, user_guest, action, expected_code):
    user_author, todo = user_employee_and_todo
    authenticate(api_client, user_guest)

    response = action(api_client, todo.pk)
    assert response.status_code == expected_code


@pytest.mark.django_db
@pytest.mark.parametrize('action, expected_code', [(put_todo, 403), (patch_todo, 403), (delete_todo, 403)])
def test_employee(api_client: APIClient, authenticate, user_employee_and_todo, user_employee, action, expected_code):
    user_author, todo = user_employee_and_todo
    authenticate(api_client, user_employee)

    response = action(api_client, todo.pk)
    assert response.status_code == expected_code


@pytest.mark.django_db
@pytest.mark.parametrize('action, expected_code', [(put_todo, 200), (patch_todo, 200), (delete_todo, 204)])
def test_author(api_client: APIClient, authenticate, user_employee_and_todo, action, expected_code):
    user_author, todo = user_employee_and_todo
    authenticate(api_client, user_author)

    response = action(api_client, todo.pk)
    assert response.status_code == expected_code


@pytest.mark.django_db
@pytest.mark.parametrize('action, expected_code', [(put_todo, 200), (patch_todo, 200), (delete_todo, 204)])
def test_admin(api_client: APIClient, authenticate, user_employee_and_todo, user_admin, action, expected_code):
    user_author, todo = user_employee_and_todo
    authenticate(api_client, user_admin)

    response = action(api_client, todo.pk)
    assert response.status_code == expected_code
