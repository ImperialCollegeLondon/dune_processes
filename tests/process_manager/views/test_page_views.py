from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from ...utils import LoginRequiredTest, PermissionRequiredTest


class TestIndexView(LoginRequiredTest):
    """Tests for the index view."""

    endpoint = reverse("process_manager:index")

    def test_authenticated(self, auth_client):
        """Test the index view for an authenticated user."""
        with assertTemplateUsed(template_name="process_manager/index.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK


class TestLogsView(PermissionRequiredTest):
    """Tests for the logs view."""

    uuid = uuid4()
    endpoint = reverse("process_manager:logs", kwargs=dict(uuid=uuid))

    def test_get(self, auth_logs_client, mocker):
        """Test the logs view for a privileged user."""
        mock = mocker.patch("process_manager.views.pages.get_process_logs")
        with assertTemplateUsed(template_name="process_manager/logs.html"):
            response = auth_logs_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        mock.assert_called_once_with(str(self.uuid))
        assert "log_text" in response.context


class TestBootProcess(PermissionRequiredTest):
    """Grouping the tests for the BootProcess view."""

    template_name = "process_manager/boot_process.html"
    endpoint = reverse("process_manager:boot_process")

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
