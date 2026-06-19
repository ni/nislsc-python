from __future__ import annotations

from unittest.mock import Mock

from nislsc.utils import flatten_names, unflatten_names


def test___flatten_names___delegates_to_interpreter(interpreter: Mock) -> None:
    interpreter.flatten_names.return_value = "Mod1,Mod2,Chassis"

    result = flatten_names(["Mod1", "Mod2", "Chassis"])

    interpreter.flatten_names.assert_called_once_with(["Mod1", "Mod2", "Chassis"])
    assert result == "Mod1,Mod2,Chassis"


def test___flatten_names___consecutive_physical_channels___collapses_to_range(
    interpreter: Mock,
) -> None:
    interpreter.flatten_names.return_value = "Mod1/load0:2"

    result = flatten_names(["Mod1/load0", "Mod1/load1", "Mod1/load2"])

    interpreter.flatten_names.assert_called_once_with(
        ["Mod1/load0", "Mod1/load1", "Mod1/load2"]
    )
    assert result == "Mod1/load0:2"


def test___flatten_names___single_name___returns_that_name(interpreter: Mock) -> None:
    interpreter.flatten_names.return_value = "Dev1"

    result = flatten_names(["Dev1"])

    interpreter.flatten_names.assert_called_once_with(["Dev1"])
    assert result == "Dev1"


def test___unflatten_names___delegates_to_interpreter(interpreter: Mock) -> None:
    interpreter.unflatten_names.return_value = ["Mod1", "Mod2", "Chassis"]

    result = unflatten_names("Mod1,Mod2,Chassis")

    interpreter.unflatten_names.assert_called_once_with("Mod1,Mod2,Chassis")
    assert result == ["Mod1", "Mod2", "Chassis"]


def test___unflatten_names___range_syntax___expands_to_list(interpreter: Mock) -> None:
    interpreter.unflatten_names.return_value = [
        "Mod1/load0",
        "Mod1/load1",
        "Mod1/load2",
    ]

    result = unflatten_names("Mod1/load0:2")

    interpreter.unflatten_names.assert_called_once_with("Mod1/load0:2")
    assert result == ["Mod1/load0", "Mod1/load1", "Mod1/load2"]


def test___unflatten_names___single_name___returns_single_element_list(
    interpreter: Mock,
) -> None:
    interpreter.unflatten_names.return_value = ["Dev1"]

    result = unflatten_names("Dev1")

    interpreter.unflatten_names.assert_called_once_with("Dev1")
    assert result == ["Dev1"]


def test___flatten_names___empty_list___returns_empty_string(interpreter: Mock) -> None:
    interpreter.flatten_names.return_value = ""

    result = flatten_names([])

    interpreter.flatten_names.assert_called_once_with([])
    assert result == ""


def test___unflatten_names___empty_string___returns_empty_list(interpreter: Mock) -> None:
    interpreter.unflatten_names.return_value = []

    result = unflatten_names("")

    interpreter.unflatten_names.assert_called_once_with("")
    assert result == []