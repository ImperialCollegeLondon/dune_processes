from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from main.views import ProcessAction


def test_index(client, admin_client, mocker):
    """Test the index view."""
    mocker.patch("main.views.get_session_info")
    with assertTemplateUsed(template_name="main/index.html"):
        response = client.get(reverse("main:index"))
    assert response.status_code == HTTPStatus.OK


def test_logs(client, mocker):
    """Test the logs view."""
    mock = mocker.patch("main.views._get_process_logs")

    uuid = uuid4()
    with assertTemplateUsed(template_name="main/logs.html"):
        response = client.get(reverse("main:logs", kwargs=dict(uuid=uuid)))
    assert response.status_code == HTTPStatus.OK

    mock.assert_called_once_with(str(uuid))
    assert "log_text" in response.context


def test_process_flush(client, mocker):
    """Test the process_flush view."""
    mock = mocker.patch("main.views._process_call")

    uuid = uuid4()
    response = client.get(reverse("main:flush", kwargs=dict(uuid=uuid)))

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse("main:index")
    mock.assert_called_once_with(str(uuid), ProcessAction.FLUSH)


class TestBootProcess:
    """Grouping the tests for the BootProcess view."""

    template_name = "main/boot_process.html"

    def test_boot_process_get(self, client):
        """Test the GET request for the BootProcess view."""
        with assertTemplateUsed(template_name=self.template_name):
            response = client.get(reverse("main:boot_process"))
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context

    def test_boot_process_post_invalid(self, client):
        """Test the POST request for the BootProcess view with invalid data."""
        with assertTemplateUsed(template_name=self.template_name):
            response = client.post(reverse("main:boot_process"), data=dict())
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context

    def test_boot_process_post_valid(self, client, dummy_session_data):
        """Test the POST request for the BootProcess view."""
        response = client.post(reverse("main:boot_process"), data=dummy_session_data)
        assert response.status_code == HTTPStatus.FOUND

        assert response.url == reverse("main:index")
