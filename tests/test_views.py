from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from main.tables import ProcessTable
from main.views import ProcessAction


class LoginRequiredTest:
    """Tests for views that require authentication."""

    endpoint: str

    def test_login_redirect(self, client):
        """Test that the view redirects to the login page."""
        response = client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FOUND

        assertRedirects(response, reverse("main:login") + f"?next={self.endpoint}")


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
        assertContains(response, "Boot</a>")

    def test_session_messages(self, auth_client, mocker):
        """Test the rendering of messages from the user session into the view."""
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.sessions.models import Session

        mocker.patch("main.views.get_session_info")
        session = Session.objects.get()
        message_data = ["message 1", "message 2"]
        store = SessionStore(session_key=session.session_key)
        store["messages"] = message_data
        store.save()

        response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        # messages have been removed from the session and added to the context
        assert response.context["messages"] == message_data
        assert "messages" not in store.load()


class TestLogsView(LoginRequiredTest):
    """Tests for the logs view."""

    uuid = uuid4()
    endpoint = reverse("main:logs", kwargs=dict(uuid=uuid))

    def test_logs_view_unprivileged(self, auth_client):
        """Test the logs view for an unprivileged user."""
        response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_logs_view_privileged(self, auth_logs_client, mocker):
        """Test the logs view for a privileged user."""
        mock = mocker.patch("main.views._get_process_logs")
        with assertTemplateUsed(template_name="main/logs.html"):
            response = auth_logs_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        mock.assert_called_once_with(str(self.uuid))
        assert "log_text" in response.context


class TestProcessActionView(LoginRequiredTest):
    """Tests for the process_action view."""

    endpoint = reverse("main:process_action")

    def test_process_action_no_action(self, auth_process_client):
        """Test process_action view with no action provided."""
        response = auth_process_client.post(self.endpoint, data={})
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("main:index")

    def test_process_action_invalid_action(self, auth_process_client):
        """Test process_action view with an invalid action."""
        response = auth_process_client.post(
            self.endpoint, data={"action": "invalid_action"}
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("main:index")

    @pytest.mark.parametrize("action", ["kill", "restart", "flush"])
    def test_process_action_valid_action(self, action, auth_process_client, mocker):
        """Test process_action view with a valid action."""
        mock = mocker.patch("main.views._process_call")
        uuids_ = [str(uuid4()), str(uuid4())]
        response = auth_process_client.post(
            self.endpoint, data={"action": action, "select": uuids_}
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("main:index")

        mock.assert_called_once_with(uuids_, ProcessAction(action))

    def test_process_action_get_unprivileged(self, auth_client):
        """Test the GET request for the process_action view (unprivileged)."""
        response = auth_client.get(reverse("main:boot_process"))
        assert response.status_code == HTTPStatus.FORBIDDEN


class TestBootProcess(LoginRequiredTest):
    """Grouping the tests for the BootProcess view."""

    template_name = "main/boot_process.html"
    endpoint = reverse("main:boot_process")

    def test_boot_process_get_unprivileged(self, auth_client):
        """Test the GET request for the BootProcess view (unprivileged)."""
        response = auth_client.get(reverse("main:boot_process"))
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_boot_process_get_privileged(self, auth_process_client):
        """Test the GET request for the BootProcess view (privileged)."""
        with assertTemplateUsed(template_name=self.template_name):
            response = auth_process_client.get(reverse("main:boot_process"))
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context
        assertContains(response, f'form action="{reverse("main:boot_process")}"')

    def test_boot_process_post_invalid(self, auth_process_client):
        """Test the POST request for the BootProcess view with invalid data."""
        with assertTemplateUsed(template_name=self.template_name):
            response = auth_process_client.post(
                reverse("main:boot_process"), data=dict()
            )
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context

    def test_boot_process_post_valid(
        self, auth_process_client, mocker, dummy_session_data
    ):
        """Test the POST request for the BootProcess view."""
        mock = mocker.patch("main.views._boot_process")
        response = auth_process_client.post(
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


class TestProcessTableView(LoginRequiredTest):
    """Test the main.views.process_table view function."""

    endpoint = reverse("main:process_table")

    @pytest.mark.parametrize("method", ("get", "post"))
    def test_method(self, method, auth_client, mocker):
        """Tests basic calls of view method."""
        self._mock_session_info(mocker, [])
        response = getattr(auth_client, method)(self.endpoint)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.context["table"], ProcessTable)

    def _mock_session_info(self, mocker, uuids):
        """Mocks views.get_session_info with ProcessInstanceList like data."""
        mock = mocker.patch("main.views.get_session_info")
        instance_mocks = [MagicMock() for uuid in uuids]
        for instance_mock, uuid in zip(instance_mocks, uuids):
            instance_mock.uuid.uuid = str(uuid)
            instance_mock.status_code = 0
        mock.data.values.__iter__.return_value = instance_mocks
        return mock

    def test_post_checked_rows(self, mocker, auth_client):
        """Tests table data is correct when post data is included."""
        all_uuids = [str(uuid4()) for _ in range(5)]
        selected_uuids = all_uuids[::2]

        self._mock_session_info(mocker, all_uuids)

        response = auth_client.post(self.endpoint, data=dict(select=selected_uuids))
        assert response.status_code == HTTPStatus.OK
        table = response.context["table"]
        assert isinstance(table, ProcessTable)

        for row in table.data.data:
            assert row["checked"] == (row["uuid"] in selected_uuids)
