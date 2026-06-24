from __future__ import annotations

from unittest.mock import Mock

from nislsc import Command, Session


def test___session_with_device___open_device_command___command_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500

    with Command.open_device_command(session, "Dev1", "Reset") as cmd:
        assert cmd._command_handle == 500
        interpreter.open_device_command.assert_called_once_with(
            session._session_handle, "Dev1", "Reset"
        )


def test___session_with_device___open_device_command___session_reference_stored(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500

    with Command.open_device_command(session, "Dev1", "Reset") as cmd:
        assert cmd._session is session
        assert cmd._interpreter is session._interpreter


def test___session_with_physical_channel___open_physical_channel_command___command_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_physical_channel_command.return_value = 501

    with Command.open_physical_channel_command(
        session, "Dev1/phys0", "SomeCmd"
    ) as cmd:
        assert cmd._command_handle == 501
        interpreter.open_physical_channel_command.assert_called_once_with(
            session._session_handle, "Dev1/phys0", "SomeCmd"
        )


def test___session_with_generic_command___open_generic_command___command_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_generic_command.return_value = 502

    with Command.open_generic_command(session, "$DefaultDevices", "SomeCmd") as cmd:
        assert cmd._command_handle == 502
        interpreter.open_generic_command.assert_called_once_with(
            session._session_handle, "$DefaultDevices", "SomeCmd"
        )


def test___open_device_command_open___close___close_command_called_with_handle(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500
    cmd = Command.open_device_command(session, "Dev1", "Reset")

    cmd.close()

    interpreter.close_command.assert_called_once_with(500)
    assert cmd._command_handle == 0


def test___open_device_command_open___close_twice___close_command_called_once(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500
    cmd = Command.open_device_command(session, "Dev1", "Reset")

    cmd.close()
    cmd.close()

    interpreter.close_command.assert_called_once_with(500)


def test___open_device_command_open___close_command___interpreter_close_command_called(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500
    cmd = Command.open_device_command(session, "Dev1", "Reset")

    cmd.close_command()

    interpreter.close_command.assert_called_once_with(500)


def test___open_device_command_open___context_manager___close_command_called_on_exit(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500

    with Command.open_device_command(session, "Dev1", "Reset"):
        interpreter.close_command.assert_not_called()

    interpreter.close_command.assert_called_once_with(500)


def test___open_device_command_open___get_command_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500
    interpreter.get_command_property_string.return_value = "Reset the device."

    with Command.open_device_command(session, "Dev1", "Reset") as cmd:
        result = cmd.get_command_property_string("Cmd.Descr")

    interpreter.get_command_property_string.assert_called_once_with(500, "Cmd.Descr")
    assert result == "Reset the device."


def test___open_device_command_open___get_command_property_string_documentation___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_command.return_value = 500
    interpreter.get_command_property_string.return_value = "Long description."

    with Command.open_device_command(session, "Dev1", "Reset") as cmd:
        result = cmd.get_command_property_string("Cmd.Doc")

    interpreter.get_command_property_string.assert_called_once_with(500, "Cmd.Doc")
    assert result == "Long description."