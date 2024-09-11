from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_index(client, auth_client, admin_client, mocker):
    """Test the index view."""
    mocker.patch("main.views.get_session_info")

    # Test with an anonymous client.
    response = client.get("/")
    assert response.status_code == 302

    # Test with an authenticated client.
    with assertTemplateUsed(template_name="main/index.html"):
        response = auth_client.get("/")
    assert response.status_code == 200

    # Test with an admin client.
    with assertTemplateUsed(template_name="main/index.html"):
        response = admin_client.get("/")
    assert response.status_code == 200


def test_logs(auth_client, mocker):
    """Test the logs view."""
    mock = mocker.patch("main.views._get_process_logs")

    uuid = uuid4()

    # Test with an authenticated client.
    with assertTemplateUsed(template_name="main/logs.html"):
        response = auth_client.get(reverse("logs", kwargs=dict(uuid=uuid)))
    assert response.status_code == 200

    mock.assert_called_once_with(str(uuid))
    assert "log_text" in response.context
