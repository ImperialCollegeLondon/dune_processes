from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from process_manager.tables import ProcessTable

from ...utils import LoginRequiredTest


class TestProcessTableView(LoginRequiredTest):
    """Test the process_manager.views.process_table view function."""

    endpoint = reverse("process_manager:process_table")

    @pytest.mark.parametrize("method", ("get", "post"))
    def test_method(self, method, auth_client, mocker):
        """Tests basic calls of view method."""
        self._mock_session_info(mocker, [])
        response = getattr(auth_client, method)(self.endpoint)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.context["table"], ProcessTable)

    def _mock_session_info(self, mocker, uuids):
        """Mocks views.get_session_info with ProcessInstanceList like data."""
        mock = mocker.patch("process_manager.views.partials.get_session_info")
        instance_mocks = [MagicMock() for uuid in uuids]
        for instance_mock, uuid in zip(instance_mocks, uuids):
            instance_mock.uuid.uuid = str(uuid)
            instance_mock.status_code = 0
        mock().data.values.__iter__.return_value = instance_mocks
        return mock

    def test_post_checked_rows(self, mocker, auth_client):
        """Tests table data is correct when post data is included."""
        all_uuids = [str(uuid4()) for _ in range(5)]
        selected_uuids = all_uuids[::2]

        self._mock_session_info(mocker, all_uuids)

        response = auth_client.post(self.endpoint, data=dict(select=selected_uuids))
        assert response.status_code == HTTPStatus.OK
        table = response.context["table"]
        assert isinstance(table, ProcessTable)

        for row in table.data.data:
            assert row["checked"] == (row["uuid"] in selected_uuids)
        assert "checked" not in table.columns["select"].attrs["th__input"]

    def test_post_header_checked(self, mocker, auth_client):
        """Tests header checkbox is checked if all rows are checked."""
        all_uuids = [str(uuid4()) for _ in range(5)]
        selected_uuids = all_uuids

        self._mock_session_info(mocker, all_uuids)

        response = auth_client.post(self.endpoint, data=dict(select=selected_uuids))
        assert response.status_code == HTTPStatus.OK
        table = response.context["table"]
        assert isinstance(table, ProcessTable)

        # All rows should be checked
        assert all(row["checked"] for row in table.data.data)

        # So header should be checked as well
        assert table.columns["select"].attrs["th__input"]["checked"] == "checked"


class TestMessagesView(LoginRequiredTest):
    """Test the process_manager.views.messages view function."""

    endpoint = reverse("process_manager:messages")

    def test_get(self, auth_client):
        """Tests basic calls of view method."""
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.sessions.models import Session

        session = Session.objects.get()
        message_data = ["message 1", "message 2"]
        store = SessionStore(session_key=session.session_key)
        store["messages"] = message_data
        store.save()

        with assertTemplateUsed("process_manager/partials/message_items.html"):
            response = auth_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK

        # messages have been removed from the session and added to the context
        assert response.context["messages"] == message_data[::-1]
        assert "messages" not in store.load()
