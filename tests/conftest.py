import pytest


@pytest.fixture
def dummy_session_data() -> dict[str, str | int]:
    """A dictionary of dummy data to populate a dummy session."""
    return dict(session_name="sess_name", n_processes=1, sleep=5, n_sleeps=4)
