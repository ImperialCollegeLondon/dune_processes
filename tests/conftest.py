"""Configuration for pytest."""

import pytest
from django.test import Client


@pytest.fixture
def auth_client(django_user_model) -> Client:
    """Return an authenticated client."""
    user = django_user_model.objects.create(username="testuser")
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def dummy_session_data() -> dict[str, str | int]:
    """A dictionary of dummy data to populate a dummy session."""
    return dict(session_name="sess_name", n_processes=1, sleep=5, n_sleeps=4)
