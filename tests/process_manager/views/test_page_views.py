from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from ...utils import LoginRequiredTest


class TestIndexView(LoginRequiredTest):
    """Tests for the index view."""

    endpoint = reverse("process_manager:index")

    def test_authenticated(self, auth_client):
        """Test the index view for an authenticated user."""
        with assertTemplateUsed(template_name="process_manager/index.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

    def test_admin(self, admin_client):
        """Test the index view for an admin user."""
        with assertTemplateUsed(template_name="process_manager/index.html"):
            response = admin_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK
        assertContains(response, "Boot</a>")

    def test_session_messages(self, auth_client):
        """Test the rendering of messages from the user session into the view."""
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.sessions.models import Session

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
    endpoint = reverse("process_manager:logs", kwargs=dict(uuid=uuid))

    def test_unprivileged(self, auth_client):
        """Test the logs view for an unprivileged user."""
        response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_privileged(self, auth_logs_client, mocker):
        """Test the logs view for a privileged user."""
        mock = mocker.patch("process_manager.views.pages.get_process_logs")
        with assertTemplateUsed(template_name="process_manager/logs.html"):
            response = auth_logs_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        mock.assert_called_once_with(str(self.uuid))
        assert "log_text" in response.context


class TestBootProcess(LoginRequiredTest):
    """Grouping the tests for the BootProcess view."""

    template_name = "process_manager/boot_process.html"
    endpoint = reverse("process_manager:boot_process")

    def test_get_unprivileged(self, auth_client):
        """Test the GET request for the BootProcess view (unprivileged)."""
        response = auth_client.get(reverse("process_manager:boot_process"))
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_get_privileged(self, auth_process_client):
        """Test the GET request for the BootProcess view (privileged)."""
        with assertTemplateUsed(template_name=self.template_name):
            response = auth_process_client.get(reverse("process_manager:boot_process"))
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context
        assertContains(
            response, f'form action="{reverse("process_manager:boot_process")}"'
        )

    def test_post_invalid(self, auth_process_client):
        """Test the POST request for the BootProcess view with invalid data."""
        with assertTemplateUsed(template_name=self.template_name):
            response = auth_process_client.post(
                reverse("process_manager:boot_process"), data=dict()
            )
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context

    def test_post_valid(self, auth_process_client, mocker, dummy_session_data):
        """Test the POST request for the BootProcess view."""
        mock = mocker.patch("process_manager.views.pages.boot_process")
        response = auth_process_client.post(
            reverse("process_manager:boot_process"), data=dummy_session_data
        )
        assert response.status_code == HTTPStatus.FOUND

        assert response.url == reverse("process_manager:index")

        mock.assert_called_once_with("root", dummy_session_data)
