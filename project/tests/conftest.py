import pytest

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from apps.todos.models import Todo
from apps.accounts.models import UserType

UserModel = get_user_model()

DEFAULT_USER_VALUES = {'username': 'username', 'password': 'password'}
DEFAULT_TODO_VALUES = {'title': 'title', 'description': 'description'}


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()

@pytest.fixture
def default_credentials():
    return DEFAULT_USER_VALUES


@pytest.fixture
def authenticate():
    def func(api_client: APIClient, user: UserModel) -> Token:
        token, created = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return token

    return func


@pytest.fixture
def user_default():
    data = DEFAULT_USER_VALUES
    user = UserModel.objects.create_user(**data)
    return user


@pytest.fixture
def user_guest():
    data = DEFAULT_USER_VALUES | {'username': 'guest'}
    user = UserModel.objects.create_user(**data)
    return user


@pytest.fixture
def user_employee():
    data = DEFAULT_USER_VALUES | {'username': 'employee', 'type': UserType.EMPLOYEE}
    user = UserModel.objects.create_user(**data)
    return user


@pytest.fixture
def user_admin():
    data = DEFAULT_USER_VALUES | {'username': 'admin'}
    user = UserModel.objects.create_superuser(**data)
    return user


@pytest.fixture
def user_employee_and_todo() -> tuple[UserModel, Todo]:
    data = DEFAULT_USER_VALUES | {'username': 'employee_with_todo', 'type': UserType.EMPLOYEE}
    user = UserModel.objects.create_user(**data)

    todo = Todo.objects.create(**DEFAULT_TODO_VALUES, author=user)
    return user, todo
