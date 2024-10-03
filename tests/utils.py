from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


class LoginRequiredTest:
    """Tests for views that require authentication."""

    endpoint: str

    def test_login_redirect(self, client):
        """Test that the view redirects to the login page."""
        response = client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FOUND

        assertRedirects(response, reverse("main:login") + f"?next={self.endpoint}")


class PermissionRequiredTest(LoginRequiredTest):
    """Tests for views that require authentication and correct user permissions."""

    def test_permission_deny(self, auth_client):
        """Test that authenticated users missing permissions are blocked."""
        response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.FORBIDDEN
