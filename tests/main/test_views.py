from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from ..utils import LoginRequiredTest


class TestIndexView(LoginRequiredTest):
    """Tests for the index view."""

    endpoint = reverse("main:index")

    def test_no_nav_links(self, client):
        """Test that the navbar does not have any nav links when not authenticated."""
        response = client.get(self.endpoint, follow=True)
        assertNotContains(response, "nav-link")

    def test_index_view_authenticated(self, auth_client):
        """Test the index view for an authenticated user."""
        with assertTemplateUsed(template_name="main/index.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        assertContains(
            response,
            f'<a class="nav-link" href="{reverse("process_manager:index")}">Process Manager</a>',  # noqa: E501
        )
        assertContains(
            response,
            f'<a href="{reverse("process_manager:index")}" class="btn btn-secondary">Process Manager</a>',  # noqa: E501
        )
        assertContains(
            response,
            f'<a class="nav-link" href="{reverse("controller:index")}">Controller</a>',
        )
        assertContains(
            response,
            f'<a href="{reverse("controller:index")}" class="btn btn-secondary">Controller</a>',  # noqa: E501
        )
