from __future__ import annotations

from unittest.mock import Mock

from nislsc.utils import flatten_names, get_library_version, unflatten_names


def test___interpreter_available___get_library_version___delegates_to_interpreter(
    interpreter: Mock,
) -> None:
    interpreter.get_library_version.return_value = 1

    result = get_library_version()

    interpreter.get_library_version.assert_called_once_with()
    assert result == 1


def test___flatten_names___delegates_to_interpreter(
    interpreter: Mock,
) -> None:
    interpreter.flatten_names.return_value = "Mod1,Mod2,Chassis"

    result = flatten_names(["Mod1", "Mod2", "Chassis"])

    interpreter.flatten_names.assert_called_once_with(["Mod1", "Mod2", "Chassis"])
    assert result == "Mod1,Mod2,Chassis"


def test___unflatten_names___delegates_to_interpreter(
    interpreter: Mock,
) -> None:
    interpreter.unflatten_names.return_value = ["Mod1", "Mod2", "Chassis"]

    result = unflatten_names("Mod1,Mod2,Chassis")

    interpreter.unflatten_names.assert_called_once_with("Mod1,Mod2,Chassis")
    assert result == ["Mod1", "Mod2", "Chassis"]
