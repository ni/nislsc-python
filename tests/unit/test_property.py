from __future__ import annotations

from unittest.mock import Mock

import pytest

from nislsc import Property, Session


def test___session_opened___open_device_property___property_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_property.return_value = 600

    with Property.open_device_property(session, "Dev1", "Dev.SerialNum") as prop:
        assert prop._property_handle == 600
        interpreter.open_device_property.assert_called_once_with(
            session._session_handle, "Dev1", "Dev.SerialNum"
        )


def test___session_opened___open_device_property___session_reference_stored(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_property.return_value = 600

    with Property.open_device_property(session, "Dev1", "Dev.SerialNum") as prop:
        assert prop._session is session
        assert prop._interpreter is session._interpreter


def test___session_opened___open_physical_channel_property___property_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_physical_channel_property.return_value = 601

    with Property.open_physical_channel_property(
        session, "Dev1/phys0", "PhysChan.SomeProp"
    ) as prop:
        assert prop._property_handle == 601
        interpreter.open_physical_channel_property.assert_called_once_with(
            session._session_handle, "Dev1/phys0", "PhysChan.SomeProp"
        )


def test___session_opened___open_driver_defined_property___property_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_driver_defined_property.return_value = 602

    with Property.open_driver_defined_property(session, "Drv.SomeProp") as prop:
        assert prop._property_handle == 602
        interpreter.open_driver_defined_property.assert_called_once_with(
            session._session_handle, "Drv.SomeProp"
        )


def test___session_opened___open_generic_property___property_handle_set(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_generic_property.return_value = 603

    with Property.open_generic_property(session, "$DefaultDevices", "Dev.SomeProp") as prop:
        assert prop._property_handle == 603
        interpreter.open_generic_property.assert_called_once_with(
            session._session_handle, "$DefaultDevices", "Dev.SomeProp"
        )


def test___session_opened___close___close_property_called_with_handle(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_property.return_value = 600
    prop = Property.open_device_property(session, "Dev1", "Dev.SerialNum")

    prop.close()

    interpreter.close_property.assert_called_once_with(600)
    assert prop._property_handle == 0


def test___session_opened___close_twice___close___close_property_called_once(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_property.return_value = 600
    prop = Property.open_device_property(session, "Dev1", "Dev.SerialNum")

    prop.close()
    prop.close()

    interpreter.close_property.assert_called_once_with(600)


def test___context_manager___close___close_property_called_on_exit(
    interpreter: Mock, session: Session
) -> None:
    interpreter.open_device_property.return_value = 600

    with Property.open_device_property(session, "Dev1", "Dev.SerialNum"):
        interpreter.close_property.assert_not_called()

    interpreter.close_property.assert_called_once_with(600)


@pytest.mark.parametrize(
    "method, prop_key, value",
    [
        ("get_property_property_bool", "Prop.IsReadable", True),
        ("get_property_property_int32", "Prop.DataType", 3),
        ("get_property_property_int32_array", "Prop.EnumValues", [1, 2, 3]),
        ("get_property_property_string", "Prop.Descr", "Serial number of the device."),
        ("get_property_property_string_array", "Prop.EnumStrings", ["ReadOnly", "ReadWrite"]),
    ],
)
def test___property_opened___get_property_property___returns_value(
    interpreter: Mock, session: Session, method: str, prop_key: str, value: object
) -> None:
    interpreter.open_device_property.return_value = 600
    getattr(interpreter, method).return_value = value

    with Property.open_device_property(session, "Dev1", "Dev.SomeProp") as prop:
        result = getattr(prop, method)(prop_key)

    getattr(interpreter, method).assert_called_once_with(600, prop_key)
    assert result == value
