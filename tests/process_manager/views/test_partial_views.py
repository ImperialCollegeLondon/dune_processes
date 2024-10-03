from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from django.urls import reverse

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
        mock.data.values.__iter__.return_value = instance_mocks
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
