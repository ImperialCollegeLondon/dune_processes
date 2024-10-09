from process_manager.process_manager_interface import boot_process


def test_boot_process(mocker, dummy_session_data):
    """Test the _boot_process function."""
    mock = mocker.patch(
        "process_manager.process_manager_interface.get_process_manager_driver"
    )
    boot_process("root", dummy_session_data)
    mock.assert_called_once()
    mock.return_value.dummy_boot.assert_called_once_with(
        user="root", **dummy_session_data
    )
