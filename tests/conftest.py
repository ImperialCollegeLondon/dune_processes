"""Configuration for pytest."""

import pytest
from django.test import Client


@pytest.fixture()
def auth_client(django_user_model):
    """Return an authenticated client."""
    username = "testuser"
    email = "testuser@domain"
    password = "password"
    user = django_user_model.objects.create_user(
        username=username, email=email, password=password
    )
    client = Client()
    client.force_login(user)
    return client
