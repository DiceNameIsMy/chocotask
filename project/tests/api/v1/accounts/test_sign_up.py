from typing import Optional

import pytest

from rest_framework.test import APIClient

from django.urls import reverse


SIGN_UP_URL = reverse('sign-up')


def create_user(api_client: APIClient, data: Optional[dict] = {}):
    default_values = {
        'username': 'test1',
        'password1': 'password1',
        'password2': 'password1',
    }
    default_values.update(data)

    data = {}
    for key, value in default_values.items():
        if value is not None:
            data[key] = value
    
    return api_client.post(path=SIGN_UP_URL, data=data)


@pytest.mark.django_db
def test_create_user(api_client: APIClient):
    response = create_user(
        api_client=api_client,
    )
    data: dict = response.data

    assert response.status_code == 201
    assert set(data.keys()) == {'user', 'expires_in', 'token'}


@pytest.mark.django_db
def test_create_user_password_mismatch(api_client: APIClient):
    response = create_user(
        api_client=api_client,
        data={
            'password2': 'password9',
        },
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_create_user_bad_username(api_client: APIClient):
    response = create_user(
        api_client=api_client,
        data={
            'username': None,
        },
    )
    assert response.status_code == 400

    response = create_user(
        api_client=api_client,
        data={
            'username': 'a' * 200,
        },
    )
    assert response.status_code == 400