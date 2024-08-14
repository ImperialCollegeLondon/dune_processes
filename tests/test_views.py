import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_index(client, admin_client):
    """Test the index view."""
    with assertTemplateUsed(template_name="main/index.html"):
        response = client.get("/")
    assert response.status_code == 200

    response = admin_client.get("/")
    assert response.status_code == 200
