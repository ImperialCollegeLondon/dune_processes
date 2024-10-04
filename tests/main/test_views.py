from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from ..utils import LoginRequiredTest


class TestIndexView(LoginRequiredTest):
    """Tests for the index view."""

    endpoint = reverse("main:index")

    def test_index_view_authenticated(self, auth_client, mocker):
        """Test the index view for an authenticated user."""
        with assertTemplateUsed(template_name="main/index.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK
