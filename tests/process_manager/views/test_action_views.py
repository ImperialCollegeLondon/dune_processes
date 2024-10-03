from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse

from process_manager.views.actions import ProcessAction

from ...utils import LoginRequiredTest


class TestProcessActionView(LoginRequiredTest):
    """Tests for the process_action view."""

    endpoint = reverse("process_manager:process_action")

    def test_no_action(self, auth_process_client):
        """Test process_action view with no action provided."""
        response = auth_process_client.post(self.endpoint, data={})
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("process_manager:index")

    def test_invalid_action(self, auth_process_client):
        """Test process_action view with an invalid action."""
        response = auth_process_client.post(
            self.endpoint, data={"action": "invalid_action"}
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("process_manager:index")

    @pytest.mark.parametrize("action", ["kill", "restart", "flush"])
    def test_valid_action(self, action, auth_process_client, mocker):
        """Test process_action view with a valid action."""
        mock = mocker.patch("process_manager.views.actions.process_call")
        uuids_ = [str(uuid4()), str(uuid4())]
        response = auth_process_client.post(
            self.endpoint, data={"action": action, "select": uuids_}
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("process_manager:index")

        mock.assert_called_once_with(uuids_, ProcessAction(action))

    def test_get_unprivileged(self, auth_client):
        """Test the GET request for the process_action view (unprivileged)."""
        response = auth_client.get(reverse("process_manager:boot_process"))
        assert response.status_code == HTTPStatus.FORBIDDEN
