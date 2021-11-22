from typing import Optional

import pytest

from rest_framework.test import APIClient

from django.urls import reverse


SIGN_UP_URL = reverse('sign-up')


def create_user(api_client: APIClient, data: dict = {}):
    return api_client.post(path=SIGN_UP_URL, data=data)


@pytest.mark.django_db
@pytest.mark.parametrize(['expected_code', 'credentials'],
    [
        (201, {'username': 'test1', 'password1': 'password', 'password2': 'password'}),
        (400, {'username': 'test1', 'password1': 'password', 'password2': 'bad_password'}),
        (400, {'username': 'test1', 'password1': 'password'}),
        (400, {'password1': 'password', 'password2': 'password'}),
        (400, {'username': 'a'*200, 'password1': 'password', 'password2': 'password'})
    ])
def test_create_user(api_client: APIClient, expected_code, credentials):
    response = create_user(api_client=api_client, data=credentials)
    
    assert response.status_code == expected_code
