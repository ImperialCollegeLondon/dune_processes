"""Configuration for pytest."""

import pytest
from django.contrib.auth.models import Permission
from django.test import Client


@pytest.fixture
def auth_client(django_user_model) -> Client:
    """Return an authenticated client."""
    user = django_user_model.objects.create(username="user")
    client = Client()
    client.force_login(user)
    return client


def _privileged_user_client(django_user_model, username, permission_name):
    user = django_user_model.objects.create(username=username)
    permission = Permission.objects.get(codename=permission_name)
    user.user_permissions.add(permission)
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def auth_process_client(django_user_model) -> Client:
    """Return a authenticated client with modify process privilege."""
    return _privileged_user_client(
        django_user_model, "process_user", "can_modify_processes"
    )


@pytest.fixture
def auth_logs_client(django_user_model) -> Client:
    """Return a authenticated client with view logs privilege."""
    return _privileged_user_client(
        django_user_model, "logs_user", "can_view_process_logs"
    )


@pytest.fixture
def dummy_session_data() -> dict[str, str | int]:
    """A dictionary of dummy data to populate a dummy session."""
    return dict(session_name="sess_name", n_processes=1, sleep=5, n_sleeps=4)


@pytest.fixture(autouse=True)
def grpc_mock(mocker):
    """Mock out the method that generates gRPC calls to external interfaces."""
    yield mocker.patch(
        "process_manager.process_manager_interface.ProcessManagerDriver.send_command_aio"
    )
