from typing import Optional

import pytest

from rest_framework.test import APIClient

from django.urls import reverse


SIGN_IN_URL = reverse('sign-in')

DEFAULT_VALUES = {
    'username': 'test',
    'password': 'password',
}


def sign_in_user(api_client: APIClient, data: Optional[dict] = {}):
    return api_client.post(path=SIGN_IN_URL, data=data)


@pytest.mark.django_db
def test_sign_in_user(api_client: APIClient, user_default, default_credentials):
    response = sign_in_user(
        api_client=api_client,
        data=default_credentials
    )
    data: dict = response.data

    assert response.status_code == 200
    assert set(data.keys()) == {'user', 'expires_in', 'token'}


@pytest.mark.django_db
def test_sign_in_user_wrong_credentials(api_client: APIClient, user_default, default_credentials):
    data = default_credentials | {'password': 'wrong_password'}
    response = sign_in_user(
        api_client=api_client,
        data=data
    )
    assert response.status_code == 401

    data = default_credentials | {'username': 'wrong_username'}
    response = sign_in_user(
        api_client=api_client,
        data=data
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_sign_in_user_missing_fields(api_client: APIClient, user_default, default_credentials):
    data: dict = default_credentials.copy()
    data.pop('username')
    response = sign_in_user(
        api_client=api_client,
        data=data
    )
    assert response.status_code == 400

    data: dict = default_credentials.copy()
    data.pop('password')
    response = sign_in_user(
        api_client=api_client,
        data=data
    )
    assert response.status_code == 400
