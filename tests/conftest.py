"""Configuration for pytest."""

import pytest
from django.contrib.auth.models import Permission
from django.test import Client


@pytest.fixture
def auth_client(django_user_model) -> Client:
    """Return an authenticated client."""
    user = django_user_model.objects.create(username="auth_user")
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def privileged_client(django_user_model) -> Client:
    """Return a privileged authenticated client."""
    user = django_user_model.objects.create(username="privileged_user")
    permission = Permission.objects.get(codename="can_boot_processes")
    user.user_permissions.add(permission)
    permission = Permission.objects.get(codename="can_restart_processes")
    user.user_permissions.add(permission)
    permission = Permission.objects.get(codename="can_flush_processes")
    user.user_permissions.add(permission)
    permission = Permission.objects.get(codename="can_kill_processes")
    user.user_permissions.add(permission)
    permission = Permission.objects.get(codename="can_view_process_logs")
    user.user_permissions.add(permission)
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def dummy_session_data() -> dict[str, str | int]:
    """A dictionary of dummy data to populate a dummy session."""
    return dict(session_name="sess_name", n_processes=1, sleep=5, n_sleeps=4)
