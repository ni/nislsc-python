from __future__ import annotations

import warnings
from unittest.mock import Mock

import pytest

from nislsc import Library, Session
from nislsc.constants import ReservationAccess, TableScaleCoercion
from nislsc.error import SLSCError, SLSCWarning
from nislsc.error_codes import SLSCErrors, SLSCWarnings
from tests.unit._session_utils import (
    expect_initialize_library,
    expect_initialize_session_with_devices,
    expect_initialize_session_with_nvmem_areas,
    expect_initialize_session_with_physical_channels,
    expect_initialize_session_without_resources,
)


def test___library_provided___initialize_session_with_devices___session_handle_is_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)

    with Session.initialize_session_with_devices(
        "Dev1",
        library=library,
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert session._session_handle == 100
        interpreter.initialize_session_with_devices.assert_called_once()


def test___library_provided___initialize_session_with_devices___owns_library_is_false(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter)

    with Session.initialize_session_with_devices(
        "Dev1",
        library=library,
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert not session._owns_library


def test___no_library___initialize_session_with_devices___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_devices(interpreter)

    with Session.initialize_session_with_devices(
        "Dev1",
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert session._owns_library
        assert session._library is not None


def test___library_provided___initialize_session_with_devices___interpreter_called_with_args(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter)
    library_handle = library._interpreter._library_handle

    with Session.initialize_session_with_devices(
        "Dev1,Dev2",
        library=library,
        connection_timeout=5.0,
        reservation_group="MyGroup",
        reservation_timeout=10.0,
    ):
        interpreter.initialize_session_with_devices.assert_called_once_with(
            library_handle,
            "Dev1,Dev2",
            5.0,
            ReservationAccess.READ_WRITE,
            "MyGroup",
            10.0,
        )


def test___interpreter_raises_error___initialize_session_with_devices___slsc_error_propagated(
    interpreter: Mock, library: Library
) -> None:
    interpreter.initialize_session_with_devices.side_effect = SLSCError(
        "Device not found.", -250806
    )

    with pytest.raises(SLSCError) as exc_info:
        Session.initialize_session_with_devices(
            "Dev1",
            library=library,
            reservation_access=ReservationAccess.NONE,
        )

    assert exc_info.value.error_code == -250806
    assert exc_info.value.error_type == SLSCErrors.DEVICE_NOT_FOUND
    assert "Device not found." in str(exc_info.value)


def test___session_opened___interpreter_raises_error___abort_session___slsc_error_propagated(
    interpreter: Mock, session: Session
) -> None:
    interpreter.abort_session.side_effect = SLSCError("Internal error.", -250800)

    with pytest.raises(SLSCError) as exc_info:
        session.abort_session()

    assert exc_info.value.error_code == -250800
    assert exc_info.value.error_type == SLSCErrors.INTERNAL


def test___session_opened___interpreter_emits_warning___connect_to_devices___slsc_warning_propagated(
    interpreter: Mock, session: Session
) -> None:
    def emit_warning(*args: object, **kwargs: object) -> None:
        warnings.warn(SLSCWarning("Scaling timestamp outdated.", 250800))

    interpreter.connect_to_devices.side_effect = emit_warning

    with pytest.warns(SLSCWarning) as warning_info:
        session.connect_to_devices("Dev1", 10.0)

    warning = warning_info[0].message
    assert isinstance(warning, SLSCWarning)
    assert warning.error_code == 250800
    assert warning.error_type == SLSCWarnings.SCALING_TIMESTAMP_OUTDATED


@pytest.mark.parametrize("status_code", [-250806, 250800, 0])
def test___session_opened___interpreter_status_code___connect_to_devices___error_or_warning_dispatched(
    interpreter: Mock, session: Session, status_code: int
) -> None:
    if status_code < 0:
        interpreter.connect_to_devices.side_effect = SLSCError("Device not found.", status_code)

        with pytest.raises(SLSCError) as exc_info:
            session.connect_to_devices("Dev1", 10.0)

        assert exc_info.value.error_code == status_code
    elif status_code > 0:

        def emit_warning(*args: object, **kwargs: object) -> None:
            warnings.warn(SLSCWarning("Scaling timestamp outdated.", status_code))

        interpreter.connect_to_devices.side_effect = emit_warning

        with pytest.warns(SLSCWarning) as warning_info:
            session.connect_to_devices("Dev1", 10.0)

        assert warning_info[0].message.error_code == status_code
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert session.connect_to_devices("Dev1", 10.0) is None


def test___library_provided___initialize_session_with_nvmem_areas___session_handle_is_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_nvmem_areas(interpreter, 200)

    with Session.initialize_session_with_nvmem_areas(
        "Area1",
        library=library,
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert session._session_handle == 200
        interpreter.initialize_session_with_nvmem_areas.assert_called_once()


def test___no_library___initialize_session_with_nvmem_areas___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_nvmem_areas(interpreter)

    with Session.initialize_session_with_nvmem_areas(
        "Area1",
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert session._owns_library


def test___library_provided___initialize_session_with_physical_channels___session_handle_is_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_physical_channels(interpreter, 300)

    with Session.initialize_session_with_physical_channels(
        "Dev1/phys0",
        library=library,
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert session._session_handle == 300
        interpreter.initialize_session_with_physical_channels.assert_called_once()


def test___no_library___initialize_session_with_physical_channels___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_physical_channels(interpreter)

    with Session.initialize_session_with_physical_channels(
        "Dev1/phys0",
        reservation_access=ReservationAccess.NONE,
    ) as session:
        assert session._owns_library


def test___library_provided___initialize_session_without_resources___session_handle_is_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_without_resources(interpreter, 400)

    with Session.initialize_session_without_resources(library=library) as session:
        assert session._session_handle == 400
        interpreter.initialize_session_without_resources.assert_called_once()


def test___no_library___initialize_session_without_resources___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_without_resources(interpreter)

    with Session.initialize_session_without_resources() as session:
        assert session._owns_library


def test___session_opened___close___close_session_called_with_handle(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.close()

    interpreter.close_session.assert_called_once_with(session_handle)
    assert session._session_handle == 0


def test___session_opened___close_twice___close___close_session_called_once(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.close()
    session.close()

    interpreter.close_session.assert_called_once_with(session_handle)


def test___context_manager___close___close_session_called_on_exit(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)

    with Session.initialize_session_with_devices(
        "Dev1",
        library=library,
        reservation_access=ReservationAccess.NONE,
    ):
        interpreter.close_session.assert_not_called()

    interpreter.close_session.assert_called_once_with(100)


def test___close_owns_library___close___finalize_library_also_called(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 1)
    expect_initialize_session_with_devices(interpreter, 100)

    session = Session.initialize_session_with_devices(
        "Dev1",
        reservation_access=ReservationAccess.NONE,
    )
    session.close()

    interpreter.close_session.assert_called_once_with(100)
    interpreter.finalize_library.assert_called_once()


def test___close_does_not_own_library___close___finalize_library_not_called(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)
    session = Session.initialize_session_with_devices(
        "Dev1",
        library=library,
        reservation_access=ReservationAccess.NONE,
    )

    session.close()

    interpreter.finalize_library.assert_not_called()


def test___session_opened___abort_session___interpreter_called(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.abort_session()

    interpreter.abort_session.assert_called_once_with(session_handle)


def test___session_opened___log_in___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.log_in("Chassis1", "admin", "secret", False, 10.0)

    interpreter.log_in.assert_called_once_with(
        session_handle, "Chassis1", "admin", "secret", 10.0, False
    )


def test___session_opened___log_out___interpreter_called_with_chassis_name(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.log_out("Chassis1")

    interpreter.log_out.assert_called_once_with(session_handle, "Chassis1")


def test___session_opened___connect_to_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.connect_to_devices("Dev1", 10.0)

    interpreter.connect_to_devices.assert_called_once_with(session_handle, "Dev1", 10.0)


def test___session_opened___disconnect_from_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.disconnect_from_devices("Dev1")

    interpreter.disconnect_from_devices.assert_called_once_with(session_handle, "Dev1")


def test___session_opened___connect_to_chassis_by_address___returns_chassis_name(
    interpreter: Mock, session: Session
) -> None:
    interpreter.connect_to_chassis_by_address.return_value = "Chassis1"
    session_handle = session._session_handle

    result = session.connect_to_chassis_by_address("192.168.1.1", "admin", "pass", 10.0)

    interpreter.connect_to_chassis_by_address.assert_called_once_with(
        session_handle, "192.168.1.1", "admin", "pass", 10.0
    )
    assert result == "Chassis1"


def test___session_opened___reserve_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.reserve_devices("Dev1", reservation_group="MyGroup", reservation_timeout=30.0)

    interpreter.reserve_devices.assert_called_once_with(
        session_handle, "Dev1", ReservationAccess.READ_WRITE, "MyGroup", 30.0
    )


def test___session_opened___unreserve_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.unreserve_devices("Dev1")

    interpreter.unreserve_devices.assert_called_once_with(session_handle, "Dev1")


def test___session_opened___reset_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.reset_devices("Dev1")

    interpreter.reset_devices.assert_called_once_with(session_handle, "Dev1")


def test___session_opened___rename_device___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.rename_device("Dev1", "Dev2")

    interpreter.rename_device.assert_called_once_with(session_handle, "Dev1", "Dev2")


def test___session_opened___add_network_chassis___returns_chassis_name(
    interpreter: Mock, session: Session
) -> None:
    interpreter.add_network_chassis.return_value = "Chassis1"
    session_handle = session._session_handle

    result = session.add_network_chassis("192.168.1.1", "admin", "pass", 10.0)

    interpreter.add_network_chassis.assert_called_once_with(
        session_handle, "192.168.1.1", "admin", "pass", 10.0
    )
    assert result == "Chassis1"


def test___session_opened___remove_chassis___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.remove_chassis("Chassis1")

    interpreter.remove_chassis.assert_called_once_with(session_handle, "Chassis1")


def test___session_opened___update_system_configuration_file___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.update_system_configuration_file("Chassis1", 5.0)

    interpreter.update_system_configuration_file.assert_called_once_with(
        session_handle, "Chassis1", 5.0
    )


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("get_device_property_bool", "Dev.IsPresent", True),
        ("get_device_property_bool_array", "Dev.Flags", [True, False, True]),
        ("get_device_property_double", "Dev.Temperature", 3.14),
        ("get_device_property_double_array", "Dev.Values", [1.0, 2.0, 3.0]),
        ("get_device_property_int32", "Dev.NumSlots", 7),
        ("get_device_property_int32_array", "Dev.Indices", [1, 2, 3]),
        ("get_device_property_int64", "Dev.Timestamp", 9999999999),
        ("get_device_property_int64_array", "Dev.Timestamps", [100, 200, 300]),
        ("get_device_property_string", "Dev.ProductName", "SLSC-99999"),
        ("get_device_property_string_array", "Dev.Modules", ["Mod1", "Mod2"]),
        ("get_device_property_uint32", "Dev.Count", 255),
        ("get_device_property_uint32_array", "Dev.Counts", [10, 20, 30]),
        ("get_device_property_uint64", "Dev.LargeCount", 18446744073709551615),
        ("get_device_property_uint64_array", "Dev.LargeCounts", [111, 222, 333]),
    ],
)
def test___session_opened___get_device_property___returns_value(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)("Dev1", prop)

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1", prop)
    assert result == value


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("set_device_property_bool", "Dev.Enabled", True),
        ("set_device_property_bool_array", "Dev.Flags", [True, False]),
        ("set_device_property_double", "Dev.Timeout", 5.0),
        ("set_device_property_double_array", "Dev.Values", [1.0, 2.0]),
        ("set_device_property_int32", "Dev.Index", 42),
        ("set_device_property_int32_array", "Dev.Indices", [1, 2, 3]),
        ("set_device_property_int64", "Dev.Timestamp", 9999999999),
        ("set_device_property_int64_array", "Dev.Timestamps", [100, 200]),
        ("set_device_property_string", "Dev.Name", "NewName"),
        ("set_device_property_string_array", "Dev.Labels", ["a", "b"]),
        ("set_device_property_uint32", "Dev.Count", 255),
        ("set_device_property_uint32_array", "Dev.Counts", [10, 20]),
        ("set_device_property_uint64", "Dev.LargeCount", 18446744073709551615),
        ("set_device_property_uint64_array", "Dev.LargeCounts", [111, 222]),
    ],
)
def test___session_opened___set_device_property___interpreter_called_with_args(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    session_handle = session._session_handle

    getattr(session, method)("Dev1", prop, value)

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1", prop, value)


@pytest.mark.parametrize(
    "method, resource, prop, value",
    [
        (
            "get_physical_channel_property_bool",
            "Dev1/phys0",
            "PhysChan.IsActive",
            False,
        ),
        (
            "get_physical_channel_property_bool_array",
            "Dev1/phys0",
            "PhysChan.Flags",
            [True, False],
        ),
        (
            "get_physical_channel_property_double",
            "Dev1/phys0",
            "PhysChan.Gain",
            3.14,
        ),
        (
            "get_physical_channel_property_double_array",
            "Dev1/phys0",
            "PhysChan.Gains",
            [1.0, 2.0],
        ),
        (
            "get_physical_channel_property_int32",
            "Dev1/phys0",
            "PhysChan.Index",
            4,
        ),
        (
            "get_physical_channel_property_int32_array",
            "Dev1/phys0",
            "PhysChan.Indices",
            [1, 2, 3],
        ),
        (
            "get_physical_channel_property_int64",
            "Dev1/phys0",
            "PhysChan.Timestamp",
            9999999999,
        ),
        (
            "get_physical_channel_property_int64_array",
            "Dev1/phys0",
            "PhysChan.Timestamps",
            [100, 200],
        ),
        (
            "get_physical_channel_property_string",
            "Dev1/phys0",
            "PhysChan.Name",
            "load0",
        ),
        (
            "get_physical_channel_property_string_array",
            "Dev1",
            "PhysChan.PhysicalChannels",
            ["load0", "load1"],
        ),
        (
            "get_physical_channel_property_uint32",
            "Dev1/phys0",
            "PhysChan.Count",
            255,
        ),
        (
            "get_physical_channel_property_uint32_array",
            "Dev1/phys0",
            "PhysChan.Counts",
            [10, 20],
        ),
        (
            "get_physical_channel_property_uint64",
            "Dev1/phys0",
            "PhysChan.LargeCount",
            18446744073709551615,
        ),
        (
            "get_physical_channel_property_uint64_array",
            "Dev1/phys0",
            "PhysChan.LargeCounts",
            [111, 222],
        ),
    ],
)
def test___session_opened___get_physical_channel_property___returns_value(
    interpreter: Mock,
    session: Session,
    method: str,
    resource: str,
    prop: str,
    value: object,
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)(resource, prop)

    getattr(interpreter, method).assert_called_once_with(session_handle, resource, prop)
    assert result == value


@pytest.mark.parametrize(
    "method, prop, value",
    [
        (
            "set_physical_channel_property_bool",
            "PhysChan.Enabled",
            True,
        ),
        (
            "set_physical_channel_property_bool_array",
            "PhysChan.Flags",
            [True, False],
        ),
        (
            "set_physical_channel_property_double",
            "PhysChan.Gain",
            3.14,
        ),
        (
            "set_physical_channel_property_double_array",
            "PhysChan.Gains",
            [1.0, 2.0],
        ),
        (
            "set_physical_channel_property_int32",
            "PhysChan.Index",
            7,
        ),
        (
            "set_physical_channel_property_int32_array",
            "PhysChan.Indices",
            [1, 2],
        ),
        (
            "set_physical_channel_property_int64",
            "PhysChan.Timestamp",
            9999999999,
        ),
        (
            "set_physical_channel_property_int64_array",
            "PhysChan.Timestamps",
            [100, 200],
        ),
        (
            "set_physical_channel_property_string",
            "PhysChan.Label",
            "MyLabel",
        ),
        (
            "set_physical_channel_property_string_array",
            "PhysChan.Labels",
            ["x", "y"],
        ),
        (
            "set_physical_channel_property_uint32",
            "PhysChan.Count",
            255,
        ),
        (
            "set_physical_channel_property_uint32_array",
            "PhysChan.Counts",
            [10, 20],
        ),
        (
            "set_physical_channel_property_uint64",
            "PhysChan.LargeCount",
            18446744073709551615,
        ),
        (
            "set_physical_channel_property_uint64_array",
            "PhysChan.LargeCounts",
            [111, 222],
        ),
    ],
)
def test___session_opened___set_physical_channel_property___interpreter_called_with_args(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    session_handle = session._session_handle

    getattr(session, method)("Dev1/phys0", prop, value)

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1/phys0", prop, value)


def test___session_opened___commit_properties_for_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_properties_for_devices("Dev1")

    interpreter.commit_properties_for_devices.assert_called_once_with(session_handle, "Dev1")


def test___session_opened___commit_properties_for_physical_channels___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_properties_for_physical_channels("Dev1/phys0")

    interpreter.commit_properties_for_physical_channels.assert_called_once_with(
        session_handle, "Dev1/phys0"
    )


def test___session_opened___commit_properties_for_session___interpreter_called(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_properties_for_session()

    interpreter.commit_properties_for_session.assert_called_once_with(session_handle)


def test___session_opened___commit_properties_generic___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_properties_generic("$DefaultDevices")

    interpreter.commit_properties_generic.assert_called_once_with(session_handle, "$DefaultDevices")


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("get_nvmem_area_property_bool", "NVMem.IsWritable", True),
        ("get_nvmem_area_property_bool_array", "NVMem.Flags", [True, False]),
        ("get_nvmem_area_property_string", "NVMem.Name", "Area1"),
        ("get_nvmem_area_property_string_array", "NVMem.Areas", ["Area1", "Area2"]),
        ("get_nvmem_area_property_uint32", "NVMem.Size", 512),
        ("get_nvmem_area_property_uint32_array", "NVMem.Counts", [10, 20, 30]),
    ],
)
def test___session_opened___get_nvmem_area_property___returns_value(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)("Area1", prop)

    getattr(interpreter, method).assert_called_once_with(session_handle, "Area1", prop)
    assert result == value


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("get_session_property_double", "Session.Timeout", 10.0),
        ("get_session_property_string", "Session.DefaultDevices", "Dev1"),
        ("get_session_property_string_array", "Session.Devices", ["Dev1", "Dev2"]),
    ],
)
def test___session_opened___get_session_property___returns_value(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)(prop)

    getattr(interpreter, method).assert_called_once_with(session_handle, prop)
    assert result == value


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("set_session_property_double", "Session.Timeout", 30.0),
        ("set_session_property_string", "Session.DefaultDevices", "Dev1"),
        ("set_session_property_string_array", "Session.Devices", ["Dev1", "Dev2"]),
    ],
)
def test___session_opened___set_session_property___interpreter_called_with_args(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    session_handle = session._session_handle

    getattr(session, method)(prop, value)

    getattr(interpreter, method).assert_called_once_with(session_handle, prop, value)


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("get_system_property_double", "System.Version", 1.5),
        ("get_system_property_string_array", "System.Devices", ["Dev1", "Chassis1"]),
        ("get_system_property_uint64", "System.Timestamp", 12345678),
    ],
)
def test___session_opened___get_system_property___returns_value(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)(prop)

    getattr(interpreter, method).assert_called_once_with(session_handle, prop)
    assert result == value


def test___session_opened___set_system_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_system_property_double("System.Timeout", 5.0)

    interpreter.set_system_property_double.assert_called_once_with(
        session_handle, "System.Timeout", 5.0
    )


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("get_generic_property_bool", "Dev.IsPresent", False),
        ("get_generic_property_bool_array", "Dev.Flags", [True, False]),
        ("get_generic_property_double", "Dev.Temperature", 3.14),
        ("get_generic_property_double_array", "Dev.Temperatures", [1.0, 2.0]),
        ("get_generic_property_int32", "Dev.NumSlots", 3),
        ("get_generic_property_int32_array", "Dev.Indices", [1, 2, 3]),
        ("get_generic_property_int64", "Dev.Timestamp", 9999999999),
        ("get_generic_property_int64_array", "Dev.Timestamps", [100, 200]),
        ("get_generic_property_string", "Dev.ProductName", "SLSC-99999"),
        ("get_generic_property_string_array", "Dev.Modules", ["Mod1", "Mod2"]),
        ("get_generic_property_uint32", "Dev.Count", 255),
        ("get_generic_property_uint32_array", "Dev.Counts", [10, 20]),
        ("get_generic_property_uint64", "Dev.LargeCount", 18446744073709551615),
        ("get_generic_property_uint64_array", "Dev.LargeCounts", [111, 222]),
    ],
)
def test___session_opened___get_generic_property___returns_value(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)("Dev1", prop)

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1", prop)
    assert result == value


@pytest.mark.parametrize(
    "method, prop, value",
    [
        ("set_generic_property_bool", "Dev.Enabled", True),
        ("set_generic_property_bool_array", "Dev.Flags", [True, False]),
        ("set_generic_property_double", "Dev.Temperature", 3.14),
        ("set_generic_property_double_array", "Dev.Temperatures", [1.0, 2.0]),
        ("set_generic_property_int32", "Dev.Index", 42),
        ("set_generic_property_int32_array", "Dev.Indices", [1, 2, 3]),
        ("set_generic_property_int64", "Dev.Timestamp", 9999999999),
        ("set_generic_property_int64_array", "Dev.Timestamps", [100, 200]),
        ("set_generic_property_string", "Dev.Name", "NewName"),
        ("set_generic_property_string_array", "Dev.Labels", ["a", "b"]),
        ("set_generic_property_uint32", "Dev.Count", 255),
        ("set_generic_property_uint32_array", "Dev.Counts", [10, 20]),
        ("set_generic_property_uint64", "Dev.LargeCount", 18446744073709551615),
        ("set_generic_property_uint64_array", "Dev.LargeCounts", [111, 222]),
    ],
)
def test___session_opened___set_generic_property___interpreter_called_with_args(
    interpreter: Mock, session: Session, method: str, prop: str, value: object
) -> None:
    session_handle = session._session_handle

    getattr(session, method)("Dev1", prop, value)

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1", prop, value)


def test___session_opened___execute_device_command___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.execute_device_command("Reset", 10.0, "Dev1")

    interpreter.execute_device_command.assert_called_once_with(
        session_handle, "Dev1", "Reset", 10.0
    )


def test___session_opened___execute_physical_channel_command___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.execute_physical_channel_command("Calibrate", 5.0, "Dev1/phys0")

    interpreter.execute_physical_channel_command.assert_called_once_with(
        session_handle, "Dev1/phys0", "Calibrate", 5.0
    )


def test___session_opened___execute_generic_command___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.execute_generic_command("$DefaultDevices", "Reset", 10.0)

    interpreter.execute_generic_command.assert_called_once_with(
        session_handle, "$DefaultDevices", "Reset", 10.0
    )


@pytest.mark.parametrize(
    "method, address, value",
    [
        ("read_register_uint8", 0x00, 0xFF),
        ("read_register_uint16", 0x02, 0xFFFF),
        ("read_register_uint32", 0x04, 0xDEADBEEF),
        ("read_register_uint64", 0x08, 0xDEADBEEFCAFEBABE),
    ],
)
def test___session_opened___read_register___returns_value(
    interpreter: Mock, session: Session, method: str, address: int, value: int
) -> None:
    getattr(interpreter, method).return_value = value
    session_handle = session._session_handle

    result = getattr(session, method)(address, "Dev1")

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1", address)
    assert result == value


@pytest.mark.parametrize(
    "method, address, value",
    [
        ("write_register_uint8", 0x00, 0xAB),
        ("write_register_uint16", 0x02, 0xABCD),
        ("write_register_uint32", 0x04, 0xDEADBEEF),
        ("write_register_uint64", 0x08, 0xDEADBEEFCAFEBABE),
    ],
)
def test___session_opened___write_register___interpreter_called_with_args(
    interpreter: Mock, session: Session, method: str, address: int, value: int
) -> None:
    session_handle = session._session_handle

    getattr(session, method)(address, value, "Dev1")

    getattr(interpreter, method).assert_called_once_with(session_handle, "Dev1", address, value)


def test___session_opened___get_nvmem_bytes___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_bytes.return_value = b"\x01\x02\x03"
    session_handle = session._session_handle

    result = session.get_nvmem_bytes("Area1", 0, 3)

    interpreter.get_nvmem_bytes.assert_called_once_with(session_handle, "Area1", 0, 3)
    assert result == b"\x01\x02\x03"


def test___session_opened___set_nvmem_bytes___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_nvmem_bytes("Area1", 0, b"\x01\x02\x03", "SN001", "pass")

    interpreter.set_nvmem_bytes.assert_called_once_with(
        session_handle, "Area1", 0, b"\x01\x02\x03", "SN001", "pass"
    )


def test___session_opened___commit_nvmem_areas___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_nvmem_areas("Area1")

    interpreter.commit_nvmem_areas.assert_called_once_with(session_handle, "Area1")


def test___session_opened___commit_nvmem_for_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_nvmem_for_devices("Dev1")

    interpreter.commit_nvmem_for_devices.assert_called_once_with(session_handle, "Dev1")


def test___session_opened___commit_nvmem_for_session___interpreter_called(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_nvmem_for_session()

    interpreter.commit_nvmem_for_session.assert_called_once_with(session_handle)


def test___session_opened___commit_nvmem_generic___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_nvmem_generic("$DefaultDevices")

    interpreter.commit_nvmem_generic.assert_called_once_with(session_handle, "$DefaultDevices")


def test___session_opened___get_linear_scaling_parameters___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_linear_scaling_parameters.return_value = (2.0, 0.5)
    session_handle = session._session_handle

    result = session.get_linear_scaling_parameters("Dev1/phys0")

    interpreter.get_linear_scaling_parameters.assert_called_once_with(session_handle, "Dev1/phys0")
    assert result == (2.0, 0.5)


def test___session_opened___get_polynomial_scaling_parameters___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_polynomial_scaling_parameters.return_value = ([1.0, 2.0], [0.5, 0.25])
    session_handle = session._session_handle

    result = session.get_polynomial_scaling_parameters("Dev1/phys0")

    interpreter.get_polynomial_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0"
    )
    assert result == ([1.0, 2.0], [0.5, 0.25])


def test___session_opened___get_table_scaling_parameters___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_table_scaling_parameters.return_value = ([0.0, 1.0], [0.0, 10.0], 0)
    session_handle = session._session_handle

    result = session.get_table_scaling_parameters("Dev1/phys0")

    interpreter.get_table_scaling_parameters.assert_called_once_with(session_handle, "Dev1/phys0")
    assert result == ([0.0, 1.0], [0.0, 10.0], 0)


def test___session_opened___get_user_defined_scaling_parameters___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_user_defined_scaling_parameters.return_value = (
        ["gain", "offset"],
        [2.0, 0.5],
    )
    session_handle = session._session_handle

    result = session.get_user_defined_scaling_parameters("Dev1/phys0")

    interpreter.get_user_defined_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0"
    )
    assert result == (["gain", "offset"], [2.0, 0.5])


def test___session_opened___get_user_defined_scaling_equation___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_user_defined_scaling_equation.return_value = "gain * x + offset"
    session_handle = session._session_handle

    result = session.get_user_defined_scaling_equation("Dev1/phys0")

    interpreter.get_user_defined_scaling_equation.assert_called_once_with(
        session_handle, "Dev1/phys0"
    )
    assert result == "gain * x + offset"


def test___session_opened___set_linear_scaling_parameters___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_linear_scaling_parameters("Dev1/phys0", 2.0, 0.5, "SN001", "pass")

    interpreter.set_linear_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0", 2.0, 0.5, "SN001", "pass"
    )


def test___session_opened___set_polynomial_scaling_parameters___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_polynomial_scaling_parameters(
        "Dev1/phys0", [1.0, 2.0], [0.5, 0.25], "SN001", "pass"
    )

    interpreter.set_polynomial_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0", [1.0, 2.0], [0.5, 0.25], "SN001", "pass"
    )


def test___session_opened___set_table_scaling_parameters___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_table_scaling_parameters(
        "Dev1/phys0",
        [0.0, 1.0],
        [0.0, 10.0],
        TableScaleCoercion.INTERPOLATE,
        "SN001",
        "pass",
    )

    interpreter.set_table_scaling_parameters.assert_called_once_with(
        session_handle,
        "Dev1/phys0",
        [0.0, 1.0],
        [0.0, 10.0],
        TableScaleCoercion.INTERPOLATE,
        "SN001",
        "pass",
    )


def test___session_opened___set_user_defined_scaling_parameters___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_user_defined_scaling_parameters(
        "Dev1/phys0", ["gain", "offset"], [2.0, 0.5], "SN001", "pass"
    )

    interpreter.set_user_defined_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0", ["gain", "offset"], [2.0, 0.5], "SN001", "pass"
    )


def test___session_opened___set_user_defined_scaling_equation___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_user_defined_scaling_equation("Dev1/phys0", "gain * x + offset", "SN001", "pass")

    interpreter.set_user_defined_scaling_equation.assert_called_once_with(
        session_handle, "Dev1/phys0", "gain * x + offset", "SN001", "pass"
    )


def test___session_opened___commit_scaling_for_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_scaling_for_devices("Dev1")

    interpreter.commit_scaling_for_devices.assert_called_once_with(session_handle, "Dev1")
