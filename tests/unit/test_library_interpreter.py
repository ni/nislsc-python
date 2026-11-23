from __future__ import annotations

import importlib
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    ("function_name", "python_method"),
    [
        ("ConnectToChassisByAddress", "connect_to_chassis_by_address"),
        ("AddNetworkChassis", "add_network_chassis"),
    ],
)
def test___side_effecting_string_function___native_call_once___returns_chassis_name(
    function_name: str,
    python_method: str,
    mocker: MockerFixture,
) -> None:
    mocker.patch("ctypes.CDLL", return_value=Mock())
    library_interpreter_module = importlib.import_module("nislsc._library_interpreter")
    native_function = mocker.patch.object(
        library_interpreter_module.lib,
        f"niSLSC_{function_name}",
        return_value=0,
    )

    def set_chassis_name(*args: object) -> int:
        setattr(args[5], "value", b"Chassis1")
        return 0

    native_function.side_effect = set_chassis_name
    interpreter = library_interpreter_module.LibraryInterpreter()
    mocker.patch.object(interpreter, "_check_for_error")

    result = getattr(interpreter, python_method)(1, "192.168.1.1", "admin", "pass", 10.0)

    native_function.assert_called_once()
    assert native_function.call_args.args[6] == 4096
    assert result == "Chassis1"
