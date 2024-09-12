from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed

from main.views import ProcessAction


def test_index(client, auth_client, admin_client, mocker):
    """Test the index view."""
    mocker.patch("main.views.get_session_info")

    # Test with an anonymous client.
    response = client.get(reverse("main:index"))
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, "/accounts/login/?next=/")

    # Test with an authenticated client.
    with assertTemplateUsed(template_name="main/index.html"):
        response = auth_client.get(reverse("main:index"))
    assert response.status_code == HTTPStatus.OK

    # Test with an admin client.
    with assertTemplateUsed(template_name="main/index.html"):
        response = admin_client.get(reverse("main:index"))
    assert response.status_code == HTTPStatus.OK

    assert "table" in response.context
    assertContains(response, "Boot</a>")


def test_logs(auth_client, mocker):
    """Test the logs view."""
    mock = mocker.patch("main.views._get_process_logs")

    uuid = uuid4()
    with assertTemplateUsed(template_name="main/logs.html"):
        response = auth_client.get(reverse("main:logs", kwargs=dict(uuid=uuid)))
    assert response.status_code == HTTPStatus.OK

    mock.assert_called_once_with(str(uuid))
    assert "log_text" in response.context


def test_process_flush(auth_client, mocker):
    """Test the process_flush view."""
    mock = mocker.patch("main.views._process_call")

    uuid = uuid4()
    response = auth_client.get(reverse("main:flush", kwargs=dict(uuid=uuid)))

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
        assertContains(response, f'form action="{reverse("main:boot_process")}"')

    def test_boot_process_post_invalid(self, client):
        """Test the POST request for the BootProcess view with invalid data."""
        with assertTemplateUsed(template_name=self.template_name):
            response = client.post(reverse("main:boot_process"), data=dict())
        assert response.status_code == HTTPStatus.OK

        assert "form" in response.context

    def test_boot_process_post_valid(self, client, mocker, dummy_session_data):
        """Test the POST request for the BootProcess view."""
        mock = mocker.patch("main.views._boot_process")
        response = client.post(reverse("main:boot_process"), data=dummy_session_data)
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
