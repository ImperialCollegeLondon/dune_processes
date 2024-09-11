"""Configuration for pytest."""

import pytest
from django.test import Client


@pytest.fixture()
def auth_client(django_user_model):
    """Return an authenticated client."""
    user = django_user_model.objects.create(username="testuser")
    client = Client()
    client.force_login(user)
    return client
