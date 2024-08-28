from pytest_django.asserts import assertTemplateUsed


def test_index(client, admin_client, mocker):
    """Test the index view."""
    mocker.patch("main.views.get_session_info")
    with assertTemplateUsed(template_name="main/index.html"):
        response = client.get("/")
    assert response.status_code == 200

    response = admin_client.get("/")
    assert response.status_code == 200
