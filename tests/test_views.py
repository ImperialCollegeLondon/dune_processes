from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_index(client, admin_client, mocker):
    """Test the index view."""
    mocker.patch("main.views.get_session_info")
    with assertTemplateUsed(template_name="main/index.html"):
        response = client.get("/")
    assert response.status_code == 200

    response = admin_client.get("/")
    assert response.status_code == 200


def test_logs(client, mocker):
    """Test the logs view."""
    mock = mocker.patch("main.views._get_process_logs")

    uuid = uuid4()
    with assertTemplateUsed(template_name="main/logs.html"):
        response = client.get(reverse("logs", kwargs=dict(uuid=uuid)))
    assert response.status_code == 200

    mock.assert_called_once_with(str(uuid))
    assert "log_text" in response.context
