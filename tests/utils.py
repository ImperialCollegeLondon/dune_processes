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
