import pytest

from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

UserModel = get_user_model()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def create_user():
    def create_user_decorator(data: dict):
        user = UserModel.objects.create_user(**data)
        return user

    return create_user_decorator


@pytest.fixture
def create_token():
    def decorator(user: UserModel):
        token, created = Token.objects.get_or_create(user=user)
        return token

    return decorator
