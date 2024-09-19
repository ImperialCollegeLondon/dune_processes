from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from main.views import ProcessAction


class LoginRequiredTest:
    """Tests for views that require authentication."""

    endpoint: str

    def test_login_redirect(self, client):
        """Test that the view redirects to the login page."""
        response = client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FOUND

        assertRedirects(response, reverse("main:login") + f"?next={self.endpoint}")


class ProcessActionsTest(LoginRequiredTest):
    """Grouping the tests for the process action views."""

    action: ProcessAction

    @classmethod
    def setup_class(cls):
        """Set up the endpoint for the tests."""
        cls.uuid = uuid4()
        cls.endpoint = reverse(f"main:{cls.action.value}", kwargs=dict(uuid=cls.uuid))

    def test_process_action_view_authenticated(self, auth_client, mocker):
        """Test the process action view for an authenticated user."""
        mock = mocker.patch("main.views._process_call")
        response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("main:index")

        mock.assert_called_once_with(str(self.uuid), self.action)


class TestIndexView(LoginRequiredTest):
    """Tests for the index view."""

    endpoint = reverse("main:index")

    def test_index_view_authenticated(self, auth_client, mocker):
        """Test the index view for an authenticated user."""
        mocker.patch("main.views.get_session_info")
        with assertTemplateUsed(template_name="main/index.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

    def test_index_view_admin(self, admin_client, mocker):
        """Test the index view for an admin user."""
        mocker.patch("main.views.get_session_info")
        with assertTemplateUsed(template_name="main/index.html"):
            response = admin_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK
        assert "table" in response.context
        assertContains(response, "Boot</a>")


class TestLogsView(LoginRequiredTest):
    """Tests for the logs view."""

    @classmethod
    def setup_class(cls):
        """Set up the endpoint for the tests."""
        cls.uuid = uuid4()
        cls.endpoint = reverse("main:logs", kwargs=dict(uuid=cls.uuid))

    def test_logs_view_authenticated(self, auth_client, mocker):
        """Test the logs view for an authenticated user."""
        mock = mocker.patch("main.views._get_process_logs")
        with assertTemplateUsed(template_name="main/logs.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        mock.assert_called_once_with(str(self.uuid))
        assert "log_text" in response.context


class TestProcessFlushView(ProcessActionsTest):
    """Tests for the process flush view."""

    action = ProcessAction.FLUSH


class TestProcessKillView(ProcessActionsTest):
    """Tests for the process kill view."""

    action = ProcessAction.KILL


class TestProcessRestartView(ProcessActionsTest):
    """Tests for the process restart view."""

    action = ProcessAction.RESTART


class TestBootProcess(LoginRequiredTest):
    """Grouping the tests for the BootProcess view."""

    template_name = "main/boot_process.html"
    endpoint = reverse("main:boot_process")

    def test_boot_process_get(self, auth_client):
        """Test the GET request for the BootProcess view."""
        with assertTemplateUsed(template_name=self.template_name):
            response = auth_client.get(reverse("main:boot_process"))
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context
        assertContains(response, f'form action="{reverse("main:boot_process")}"')

    def test_boot_process_post_invalid(self, auth_client):
        """Test the POST request for the BootProcess view with invalid data."""
        with assertTemplateUsed(template_name=self.template_name):
            response = auth_client.post(reverse("main:boot_process"), data=dict())
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context

    def test_boot_process_post_valid(self, auth_client, mocker, dummy_session_data):
        """Test the POST request for the BootProcess view."""
        mock = mocker.patch("main.views._boot_process")
        response = auth_client.post(
            reverse("main:boot_process"), data=dummy_session_data
        )
        assert response.status_code == HTTPStatus.FOUND

        assert response.url == reverse("main:index")

        mock.assert_called_once_with("root", dummy_session_data)


@pytest.mark.asyncio
async def test_boot_process(mocker, dummy_session_data):
    """Test the _boot_process function."""
    from main.views import _boot_process

    mock = mocker.patch("main.views.get_process_manager_driver")
    await _boot_process("root", dummy_session_data)
    mock.assert_called_once()
    mock.return_value.dummy_boot.assert_called_once_with(
        user="root", **dummy_session_data
    )
