from typing import Optional

import pytest

from rest_framework.test import APIClient

from django.urls import reverse


SIGN_IN_URL = reverse('sign-in')

DEFAULT_VALUES = {
    'username': 'test1',
    'password': 'password1',
}


def sign_in_user(api_client: APIClient, data: Optional[dict] = {}):
    default_values = DEFAULT_VALUES

    default_values.update(data)

    data = {}
    for key, value in default_values.items():
        if value is not None:
            data[key] = value

    return api_client.post(path=SIGN_IN_URL, data=data)


@pytest.mark.django_db
def test_sign_in_user(api_client: APIClient, create_user):
    create_user(DEFAULT_VALUES)
    response = sign_in_user(
        api_client=api_client,
    )
    data: dict = response.data

    assert response.status_code == 200
    assert set(data.keys()) == {'user', 'expires_in', 'token'}


@pytest.mark.django_db
def test_sign_in_user_wrong_credentials(api_client: APIClient, create_user):
    create_user(DEFAULT_VALUES)

    response = sign_in_user(
        api_client=api_client,
        data={
            'password': 'wrong_password',
        },
    )
    assert response.status_code == 401
    response = sign_in_user(
        api_client=api_client,
        data={
            'password': 'wrong_username',
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_sign_in_user_missing_fields(api_client: APIClient, create_user):
    create_user(DEFAULT_VALUES)

    response = sign_in_user(
        api_client=api_client,
        data={
            'username': None,
        },
    )
    assert response.status_code == 400

    response = sign_in_user(
        api_client=api_client,
        data={
            'password': None
        },
    )
    assert response.status_code == 400
