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
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._session_handle == 100
        interpreter.initialize_session_with_devices.assert_called_once()


def test___library_provided___initialize_session_with_devices___owns_library_is_false(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter)

    with Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert not session._owns_library


def test___no_library___initialize_session_with_devices___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_devices(interpreter)

    with Session.initialize_session_with_devices(
        None, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._owns_library
        assert session._library is not None


def test___library_provided___initialize_session_with_devices___interpreter_called_with_args(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter)
    library_handle = library._interpreter._library_handle

    with Session.initialize_session_with_devices(
        library, "Dev1,Dev2", 5.0, ReservationAccess.READ_WRITE, "MyGroup", 10.0
    ):
        interpreter.initialize_session_with_devices.assert_called_once_with(
            library_handle, "Dev1,Dev2", 5.0, ReservationAccess.READ_WRITE, "MyGroup", 10.0
        )

        
def test___interpreter_raises_error___initialize_session_with_devices___slsc_error_propagated(
    interpreter: Mock, library: Library
) -> None:
    interpreter.initialize_session_with_devices.side_effect = SLSCError(
        "Device not found.", -250806
    )

    with pytest.raises(SLSCError) as exc_info:
        Session.initialize_session_with_devices(
            library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
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
        library, "Area1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._session_handle == 200
        interpreter.initialize_session_with_nvmem_areas.assert_called_once()


def test___no_library___initialize_session_with_nvmem_areas___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_nvmem_areas(interpreter)

    with Session.initialize_session_with_nvmem_areas(
        None, "Area1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._owns_library


def test___library_provided___initialize_session_with_physical_channels___session_handle_is_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_physical_channels(interpreter, 300)

    with Session.initialize_session_with_physical_channels(
        library, "Dev1/phys0", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._session_handle == 300
        interpreter.initialize_session_with_physical_channels.assert_called_once()


def test___no_library___initialize_session_with_physical_channels___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_physical_channels(interpreter)

    with Session.initialize_session_with_physical_channels(
        None, "Dev1/phys0", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._owns_library


def test___library_provided___initialize_session_without_resources___session_handle_is_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_without_resources(interpreter, 400)

    with Session.initialize_session_without_resources(library) as session:
        assert session._session_handle == 400
        interpreter.initialize_session_without_resources.assert_called_once()


def test___no_library___initialize_session_without_resources___library_created_and_owned(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_without_resources(interpreter)

    with Session.initialize_session_without_resources(None) as session:
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
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ):
        interpreter.close_session.assert_not_called()

    interpreter.close_session.assert_called_once_with(100)


def test___close_owns_library___close___finalize_library_also_called(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 1)
    expect_initialize_session_with_devices(interpreter, 100)

    session = Session.initialize_session_with_devices(
        None, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    )
    session.close()

    interpreter.close_session.assert_called_once_with(100)
    interpreter.finalize_library.assert_called_once()


def test___close_does_not_own_library___close___finalize_library_not_called(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)
    session = Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    )

    session.close()

    interpreter.finalize_library.assert_not_called()


def test___session_opened___abort_session___interpreter_called(interpreter: Mock, session: Session) -> None:
    session_handle = session._session_handle

    session.abort_session()

    interpreter.abort_session.assert_called_once_with(session_handle)


def test___session_opened___log_in___interpreter_called_with_args(interpreter: Mock, session: Session) -> None:
    session_handle = session._session_handle

    session.log_in("Chassis1", "admin", "secret", 10.0, False)

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

    session.reserve_devices("Dev1", ReservationAccess.READ_WRITE, "MyGroup", 30.0)

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


def test___session_opened___get_device_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_bool.return_value = True
    session_handle = session._session_handle

    result = session.get_device_property_bool("Dev1", "Dev.IsPresent")

    interpreter.get_device_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.IsPresent"
    )
    assert result is True


def test___session_opened___get_device_property_bool_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_bool_array.return_value = [True, False, True]
    session_handle = session._session_handle

    result = session.get_device_property_bool_array("Dev1", "Dev.Flags")

    interpreter.get_device_property_bool_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Flags"
    )
    assert result == [True, False, True]


def test___session_opened___get_device_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_double.return_value = 3.14
    session_handle = session._session_handle

    result = session.get_device_property_double("Dev1", "Dev.Temperature")

    interpreter.get_device_property_double.assert_called_once_with(
        session_handle, "Dev1", "Dev.Temperature"
    )
    assert result == 3.14


def test___session_opened___get_device_property_double_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_double_array.return_value = [1.0, 2.0, 3.0]
    session_handle = session._session_handle

    result = session.get_device_property_double_array("Dev1", "Dev.Values")

    interpreter.get_device_property_double_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Values"
    )
    assert result == [1.0, 2.0, 3.0]


def test___session_opened___get_device_property_int32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_int32.return_value = 7
    session_handle = session._session_handle

    result = session.get_device_property_int32("Dev1", "Dev.NumSlots")

    interpreter.get_device_property_int32.assert_called_once_with(
        session_handle, "Dev1", "Dev.NumSlots"
    )
    assert result == 7


def test___session_opened___get_device_property_int32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_int32_array.return_value = [1, 2, 3]
    session_handle = session._session_handle

    result = session.get_device_property_int32_array("Dev1", "Dev.Indices")

    interpreter.get_device_property_int32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Indices"
    )
    assert result == [1, 2, 3]


def test___session_opened___get_device_property_int64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_int64.return_value = 9999999999
    session_handle = session._session_handle

    result = session.get_device_property_int64("Dev1", "Dev.Timestamp")

    interpreter.get_device_property_int64.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamp"
    )
    assert result == 9999999999


def test___session_opened___get_device_property_int64_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_int64_array.return_value = [100, 200, 300]
    session_handle = session._session_handle

    result = session.get_device_property_int64_array("Dev1", "Dev.Timestamps")

    interpreter.get_device_property_int64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamps"
    )
    assert result == [100, 200, 300]


def test___session_opened___get_device_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_string.return_value = "SLSC-99999"
    session_handle = session._session_handle

    result = session.get_device_property_string("Dev1", "Dev.ProductName")

    interpreter.get_device_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.ProductName"
    )
    assert result == "SLSC-99999"


def test___session_opened___get_device_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_string_array.return_value = ["Mod1", "Mod2"]
    session_handle = session._session_handle

    result = session.get_device_property_string_array("Dev1", "Dev.Modules")

    interpreter.get_device_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Modules"
    )
    assert result == ["Mod1", "Mod2"]


def test___session_opened___get_device_property_uint32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_uint32.return_value = 255
    session_handle = session._session_handle

    result = session.get_device_property_uint32("Dev1", "Dev.Count")

    interpreter.get_device_property_uint32.assert_called_once_with(
        session_handle, "Dev1", "Dev.Count"
    )
    assert result == 255


def test___session_opened___get_device_property_uint32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_uint32_array.return_value = [10, 20, 30]
    session_handle = session._session_handle

    result = session.get_device_property_uint32_array("Dev1", "Dev.Counts")

    interpreter.get_device_property_uint32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Counts"
    )
    assert result == [10, 20, 30]


def test___session_opened___get_device_property_uint64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_uint64.return_value = 18446744073709551615
    session_handle = session._session_handle

    result = session.get_device_property_uint64("Dev1", "Dev.LargeCount")

    interpreter.get_device_property_uint64.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCount"
    )
    assert result == 18446744073709551615


def test___session_opened___get_device_property_uint64_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_uint64_array.return_value = [111, 222, 333]
    session_handle = session._session_handle

    result = session.get_device_property_uint64_array("Dev1", "Dev.LargeCounts")

    interpreter.get_device_property_uint64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCounts"
    )
    assert result == [111, 222, 333]


def test___session_opened___set_device_property_bool___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_bool("Dev1", "Dev.Enabled", True)

    interpreter.set_device_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.Enabled", True
    )


def test___session_opened___set_device_property_bool_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_bool_array("Dev1", "Dev.Flags", [True, False])

    interpreter.set_device_property_bool_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Flags", [True, False]
    )


def test___session_opened___set_device_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_double("Dev1", "Dev.Timeout", 5.0)

    interpreter.set_device_property_double.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timeout", 5.0
    )


def test___session_opened___set_device_property_double_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_double_array("Dev1", "Dev.Values", [1.0, 2.0])

    interpreter.set_device_property_double_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Values", [1.0, 2.0]
    )


def test___session_opened___set_device_property_int32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_int32("Dev1", "Dev.Index", 42)

    interpreter.set_device_property_int32.assert_called_once_with(
        session_handle, "Dev1", "Dev.Index", 42
    )


def test___session_opened___set_device_property_int32_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_int32_array("Dev1", "Dev.Indices", [1, 2, 3])

    interpreter.set_device_property_int32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Indices", [1, 2, 3]
    )


def test___session_opened___set_device_property_int64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_int64("Dev1", "Dev.Timestamp", 9999999999)

    interpreter.set_device_property_int64.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamp", 9999999999
    )


def test___session_opened___set_device_property_int64_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_int64_array("Dev1", "Dev.Timestamps", [100, 200])

    interpreter.set_device_property_int64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamps", [100, 200]
    )


def test___session_opened___set_device_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_string("Dev1", "Dev.Name", "NewName")

    interpreter.set_device_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.Name", "NewName"
    )


def test___session_opened___set_device_property_string_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_string_array("Dev1", "Dev.Labels", ["a", "b"])

    interpreter.set_device_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Labels", ["a", "b"]
    )


def test___session_opened___set_device_property_uint32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_uint32("Dev1", "Dev.Count", 255)

    interpreter.set_device_property_uint32.assert_called_once_with(
        session_handle, "Dev1", "Dev.Count", 255
    )


def test___session_opened___set_device_property_uint32_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_uint32_array("Dev1", "Dev.Counts", [10, 20])

    interpreter.set_device_property_uint32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Counts", [10, 20]
    )


def test___session_opened___set_device_property_uint64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_uint64("Dev1", "Dev.LargeCount", 18446744073709551615)

    interpreter.set_device_property_uint64.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCount", 18446744073709551615
    )


def test___session_opened___set_device_property_uint64_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_uint64_array("Dev1", "Dev.LargeCounts", [111, 222])

    interpreter.set_device_property_uint64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCounts", [111, 222]
    )


def test___session_opened___get_physical_channel_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_bool.return_value = False
    session_handle = session._session_handle

    result = session.get_physical_channel_property_bool("Dev1/phys0", "PhysChan.IsActive")

    interpreter.get_physical_channel_property_bool.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.IsActive"
    )
    assert result is False


def test___session_opened___get_physical_channel_property_bool_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_bool_array.return_value = [True, False]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_bool_array("Dev1/phys0", "PhysChan.Flags")

    interpreter.get_physical_channel_property_bool_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Flags"
    )
    assert result == [True, False]


def test___session_opened___get_physical_channel_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_double.return_value = 3.14
    session_handle = session._session_handle

    result = session.get_physical_channel_property_double("Dev1/phys0", "PhysChan.Gain")

    interpreter.get_physical_channel_property_double.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Gain"
    )
    assert result == 3.14


def test___session_opened___get_physical_channel_property_double_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_double_array.return_value = [1.0, 2.0]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_double_array("Dev1/phys0", "PhysChan.Gains")

    interpreter.get_physical_channel_property_double_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Gains"
    )
    assert result == [1.0, 2.0]


def test___session_opened___get_physical_channel_property_int32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_int32.return_value = 4
    session_handle = session._session_handle

    result = session.get_physical_channel_property_int32("Dev1/phys0", "PhysChan.Index")

    interpreter.get_physical_channel_property_int32.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Index"
    )
    assert result == 4


def test___session_opened___get_physical_channel_property_int32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_int32_array.return_value = [1, 2, 3]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_int32_array("Dev1/phys0", "PhysChan.Indices")

    interpreter.get_physical_channel_property_int32_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Indices"
    )
    assert result == [1, 2, 3]


def test___session_opened___get_physical_channel_property_int64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_int64.return_value = 9999999999
    session_handle = session._session_handle

    result = session.get_physical_channel_property_int64("Dev1/phys0", "PhysChan.Timestamp")

    interpreter.get_physical_channel_property_int64.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Timestamp"
    )
    assert result == 9999999999


def test___session_opened___get_physical_channel_property_int64_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_int64_array.return_value = [100, 200]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_int64_array("Dev1/phys0", "PhysChan.Timestamps")

    interpreter.get_physical_channel_property_int64_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Timestamps"
    )
    assert result == [100, 200]


def test___session_opened___get_physical_channel_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_string.return_value = "load0"
    session_handle = session._session_handle

    result = session.get_physical_channel_property_string("Dev1/phys0", "PhysChan.Name")

    interpreter.get_physical_channel_property_string.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Name"
    )
    assert result == "load0"


def test___session_opened___get_physical_channel_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_string_array.return_value = ["load0", "load1"]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_string_array(
        "Dev1", "PhysChan.PhysicalChannels"
    )

    interpreter.get_physical_channel_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "PhysChan.PhysicalChannels"
    )
    assert result == ["load0", "load1"]


def test___session_opened___get_physical_channel_property_uint32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_uint32.return_value = 255
    session_handle = session._session_handle

    result = session.get_physical_channel_property_uint32("Dev1/phys0", "PhysChan.Count")

    interpreter.get_physical_channel_property_uint32.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Count"
    )
    assert result == 255


def test___session_opened___get_physical_channel_property_uint32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_uint32_array.return_value = [10, 20]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_uint32_array("Dev1/phys0", "PhysChan.Counts")

    interpreter.get_physical_channel_property_uint32_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Counts"
    )
    assert result == [10, 20]


def test___session_opened___get_physical_channel_property_uint64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_uint64.return_value = 18446744073709551615
    session_handle = session._session_handle

    result = session.get_physical_channel_property_uint64("Dev1/phys0", "PhysChan.LargeCount")

    interpreter.get_physical_channel_property_uint64.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.LargeCount"
    )
    assert result == 18446744073709551615


def test___session_opened___get_physical_channel_property_uint64_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_uint64_array.return_value = [111, 222]
    session_handle = session._session_handle

    result = session.get_physical_channel_property_uint64_array("Dev1/phys0", "PhysChan.LargeCounts")

    interpreter.get_physical_channel_property_uint64_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.LargeCounts"
    )
    assert result == [111, 222]


def test___session_opened___set_physical_channel_property_bool___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_bool("Dev1/phys0", "PhysChan.Enabled", True)

    interpreter.set_physical_channel_property_bool.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Enabled", True
    )


def test___session_opened___set_physical_channel_property_bool_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_bool_array("Dev1/phys0", "PhysChan.Flags", [True, False])

    interpreter.set_physical_channel_property_bool_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Flags", [True, False]
    )


def test___session_opened___set_physical_channel_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_double("Dev1/phys0", "PhysChan.Gain", 3.14)

    interpreter.set_physical_channel_property_double.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Gain", 3.14
    )


def test___session_opened___set_physical_channel_property_double_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_double_array("Dev1/phys0", "PhysChan.Gains", [1.0, 2.0])

    interpreter.set_physical_channel_property_double_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Gains", [1.0, 2.0]
    )


def test___session_opened___set_physical_channel_property_int32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_int32("Dev1/phys0", "PhysChan.Index", 7)

    interpreter.set_physical_channel_property_int32.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Index", 7
    )


def test___session_opened___set_physical_channel_property_int32_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_int32_array("Dev1/phys0", "PhysChan.Indices", [1, 2])

    interpreter.set_physical_channel_property_int32_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Indices", [1, 2]
    )


def test___session_opened___set_physical_channel_property_int64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_int64("Dev1/phys0", "PhysChan.Timestamp", 9999999999)

    interpreter.set_physical_channel_property_int64.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Timestamp", 9999999999
    )


def test___session_opened___set_physical_channel_property_int64_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_int64_array("Dev1/phys0", "PhysChan.Timestamps", [100, 200])

    interpreter.set_physical_channel_property_int64_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Timestamps", [100, 200]
    )


def test___session_opened___set_physical_channel_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_string("Dev1/phys0", "PhysChan.Label", "MyLabel")

    interpreter.set_physical_channel_property_string.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Label", "MyLabel"
    )


def test___session_opened___set_physical_channel_property_string_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_string_array("Dev1/phys0", "PhysChan.Labels", ["x", "y"])

    interpreter.set_physical_channel_property_string_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Labels", ["x", "y"]
    )


def test___session_opened___set_physical_channel_property_uint32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_uint32("Dev1/phys0", "PhysChan.Count", 255)

    interpreter.set_physical_channel_property_uint32.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Count", 255
    )


def test___session_opened___set_physical_channel_property_uint32_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_uint32_array("Dev1/phys0", "PhysChan.Counts", [10, 20])

    interpreter.set_physical_channel_property_uint32_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Counts", [10, 20]
    )


def test___session_opened___set_physical_channel_property_uint64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_uint64("Dev1/phys0", "PhysChan.LargeCount", 18446744073709551615)

    interpreter.set_physical_channel_property_uint64.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.LargeCount", 18446744073709551615
    )


def test___session_opened___set_physical_channel_property_uint64_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_uint64_array("Dev1/phys0", "PhysChan.LargeCounts", [111, 222])

    interpreter.set_physical_channel_property_uint64_array.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.LargeCounts", [111, 222]
    )


def test___session_opened___commit_properties_for_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_properties_for_devices("Dev1")

    interpreter.commit_properties_for_devices.assert_called_once_with(
        session_handle, "Dev1"
    )


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

    interpreter.commit_properties_generic.assert_called_once_with(
        session_handle, "$DefaultDevices"
    )


def test___session_opened___get_nvmem_area_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_bool.return_value = True
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_bool("Area1", "NVMem.IsWritable")

    interpreter.get_nvmem_area_property_bool.assert_called_once_with(
        session_handle, "Area1", "NVMem.IsWritable"
    )
    assert result is True


def test___session_opened___get_nvmem_area_property_bool_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_bool_array.return_value = [True, False]
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_bool_array("Area1", "NVMem.Flags")

    interpreter.get_nvmem_area_property_bool_array.assert_called_once_with(
        session_handle, "Area1", "NVMem.Flags"
    )
    assert result == [True, False]


def test___session_opened___get_nvmem_area_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_string.return_value = "Area1"
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_string("Area1", "NVMem.Name")

    interpreter.get_nvmem_area_property_string.assert_called_once_with(
        session_handle, "Area1", "NVMem.Name"
    )
    assert result == "Area1"


def test___session_opened___get_nvmem_area_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_string_array.return_value = ["Area1", "Area2"]
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_string_array("Area1", "NVMem.Areas")

    interpreter.get_nvmem_area_property_string_array.assert_called_once_with(
        session_handle, "Area1", "NVMem.Areas"
    )
    assert result == ["Area1", "Area2"]


def test___session_opened___get_nvmem_area_property_uint32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_uint32.return_value = 512
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_uint32("Area1", "NVMem.Size")

    interpreter.get_nvmem_area_property_uint32.assert_called_once_with(
        session_handle, "Area1", "NVMem.Size"
    )
    assert result == 512


def test___session_opened___get_nvmem_area_property_uint32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_uint32_array.return_value = [10, 20, 30]
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_uint32_array("Area1", "NVMem.Counts")

    interpreter.get_nvmem_area_property_uint32_array.assert_called_once_with(
        session_handle, "Area1", "NVMem.Counts"
    )
    assert result == [10, 20, 30]


def test___session_opened___get_session_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_session_property_double.return_value = 10.0
    session_handle = session._session_handle

    result = session.get_session_property_double("Session.Timeout")

    interpreter.get_session_property_double.assert_called_once_with(
        session_handle, "Session.Timeout"
    )
    assert result == 10.0


def test___session_opened___get_session_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_session_property_string.return_value = "Dev1"
    session_handle = session._session_handle

    result = session.get_session_property_string("Session.DefaultDevices")

    interpreter.get_session_property_string.assert_called_once_with(
        session_handle, "Session.DefaultDevices"
    )
    assert result == "Dev1"


def test___session_opened___get_session_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_session_property_string_array.return_value = ["Dev1", "Dev2"]
    session_handle = session._session_handle

    result = session.get_session_property_string_array("Session.Devices")

    interpreter.get_session_property_string_array.assert_called_once_with(
        session_handle, "Session.Devices"
    )
    assert result == ["Dev1", "Dev2"]


def test___session_opened___set_session_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_session_property_double("Session.Timeout", 30.0)

    interpreter.set_session_property_double.assert_called_once_with(
        session_handle, "Session.Timeout", 30.0
    )


def test___session_opened___set_session_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_session_property_string("Session.DefaultDevices", "Dev1")

    interpreter.set_session_property_string.assert_called_once_with(
        session_handle, "Session.DefaultDevices", "Dev1"
    )


def test___session_opened___set_session_property_string_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_session_property_string_array("Session.Devices", ["Dev1", "Dev2"])

    interpreter.set_session_property_string_array.assert_called_once_with(
        session_handle, "Session.Devices", ["Dev1", "Dev2"]
    )


def test___session_opened___get_system_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_system_property_double.return_value = 1.5
    session_handle = session._session_handle

    result = session.get_system_property_double("System.Version")

    interpreter.get_system_property_double.assert_called_once_with(
        session_handle, "System.Version"
    )
    assert result == 1.5


def test___session_opened___get_system_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_system_property_string_array.return_value = ["Dev1", "Chassis1"]
    session_handle = session._session_handle

    result = session.get_system_property_string_array("System.Devices")

    interpreter.get_system_property_string_array.assert_called_once_with(
        session_handle, "System.Devices"
    )
    assert result == ["Dev1", "Chassis1"]


def test___session_opened___get_system_property_uint64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_system_property_uint64.return_value = 12345678
    session_handle = session._session_handle

    result = session.get_system_property_uint64("System.Timestamp")

    interpreter.get_system_property_uint64.assert_called_once_with(
        session_handle, "System.Timestamp"
    )
    assert result == 12345678


def test___session_opened___set_system_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_system_property_double("System.Timeout", 5.0)

    interpreter.set_system_property_double.assert_called_once_with(
        session_handle, "System.Timeout", 5.0
    )


def test___session_opened___get_generic_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_bool.return_value = False
    session_handle = session._session_handle

    result = session.get_generic_property_bool("Dev1", "Dev.IsPresent")

    interpreter.get_generic_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.IsPresent"
    )
    assert result is False


def test___session_opened___get_generic_property_bool_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_bool_array.return_value = [True, False]
    session_handle = session._session_handle

    result = session.get_generic_property_bool_array("Dev1", "Dev.Flags")

    interpreter.get_generic_property_bool_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Flags"
    )
    assert result == [True, False]


def test___session_opened___get_generic_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_double.return_value = 3.14
    session_handle = session._session_handle

    result = session.get_generic_property_double("Dev1", "Dev.Temperature")

    interpreter.get_generic_property_double.assert_called_once_with(
        session_handle, "Dev1", "Dev.Temperature"
    )
    assert result == 3.14


def test___session_opened___get_generic_property_double_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_double_array.return_value = [1.0, 2.0]
    session_handle = session._session_handle

    result = session.get_generic_property_double_array("Dev1", "Dev.Temperatures")

    interpreter.get_generic_property_double_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Temperatures"
    )
    assert result == [1.0, 2.0]


def test___session_opened___get_generic_property_int32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_int32.return_value = 3
    session_handle = session._session_handle

    result = session.get_generic_property_int32("Dev1", "Dev.NumSlots")

    interpreter.get_generic_property_int32.assert_called_once_with(
        session_handle, "Dev1", "Dev.NumSlots"
    )
    assert result == 3


def test___session_opened___get_generic_property_int32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_int32_array.return_value = [1, 2, 3]
    session_handle = session._session_handle

    result = session.get_generic_property_int32_array("Dev1", "Dev.Indices")

    interpreter.get_generic_property_int32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Indices"
    )
    assert result == [1, 2, 3]


def test___session_opened___get_generic_property_int64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_int64.return_value = 9999999999
    session_handle = session._session_handle

    result = session.get_generic_property_int64("Dev1", "Dev.Timestamp")

    interpreter.get_generic_property_int64.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamp"
    )
    assert result == 9999999999


def test___session_opened___get_generic_property_int64_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_int64_array.return_value = [100, 200]
    session_handle = session._session_handle

    result = session.get_generic_property_int64_array("Dev1", "Dev.Timestamps")

    interpreter.get_generic_property_int64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamps"
    )
    assert result == [100, 200]


def test___session_opened___get_generic_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_string.return_value = "SLSC-99999"
    session_handle = session._session_handle

    result = session.get_generic_property_string("Dev1", "Dev.ProductName")

    interpreter.get_generic_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.ProductName"
    )
    assert result == "SLSC-99999"


def test___session_opened___get_generic_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_string_array.return_value = ["Mod1", "Mod2"]
    session_handle = session._session_handle

    result = session.get_generic_property_string_array("Dev1", "Dev.Modules")

    interpreter.get_generic_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Modules"
    )
    assert result == ["Mod1", "Mod2"]


def test___session_opened___get_generic_property_uint32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_uint32.return_value = 255
    session_handle = session._session_handle

    result = session.get_generic_property_uint32("Dev1", "Dev.Count")

    interpreter.get_generic_property_uint32.assert_called_once_with(
        session_handle, "Dev1", "Dev.Count"
    )
    assert result == 255


def test___session_opened___get_generic_property_uint32_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_uint32_array.return_value = [10, 20]
    session_handle = session._session_handle

    result = session.get_generic_property_uint32_array("Dev1", "Dev.Counts")

    interpreter.get_generic_property_uint32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Counts"
    )
    assert result == [10, 20]


def test___session_opened___get_generic_property_uint64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_uint64.return_value = 18446744073709551615
    session_handle = session._session_handle

    result = session.get_generic_property_uint64("Dev1", "Dev.LargeCount")

    interpreter.get_generic_property_uint64.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCount"
    )
    assert result == 18446744073709551615


def test___session_opened___get_generic_property_uint64_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_uint64_array.return_value = [111, 222]
    session_handle = session._session_handle

    result = session.get_generic_property_uint64_array("Dev1", "Dev.LargeCounts")

    interpreter.get_generic_property_uint64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCounts"
    )
    assert result == [111, 222]


def test___session_opened___set_generic_property_bool___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_bool("Dev1", "Dev.Enabled", True)

    interpreter.set_generic_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.Enabled", True
    )


def test___session_opened___set_generic_property_bool_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_bool_array("Dev1", "Dev.Flags", [True, False])

    interpreter.set_generic_property_bool_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Flags", [True, False]
    )


def test___session_opened___set_generic_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_double("Dev1", "Dev.Temperature", 3.14)

    interpreter.set_generic_property_double.assert_called_once_with(
        session_handle, "Dev1", "Dev.Temperature", 3.14
    )


def test___session_opened___set_generic_property_double_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_double_array("Dev1", "Dev.Temperatures", [1.0, 2.0])

    interpreter.set_generic_property_double_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Temperatures", [1.0, 2.0]
    )


def test___session_opened___set_generic_property_int32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_int32("Dev1", "Dev.Index", 42)

    interpreter.set_generic_property_int32.assert_called_once_with(
        session_handle, "Dev1", "Dev.Index", 42
    )


def test___session_opened___set_generic_property_int32_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_int32_array("Dev1", "Dev.Indices", [1, 2, 3])

    interpreter.set_generic_property_int32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Indices", [1, 2, 3]
    )


def test___session_opened___set_generic_property_int64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_int64("Dev1", "Dev.Timestamp", 9999999999)

    interpreter.set_generic_property_int64.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamp", 9999999999
    )


def test___session_opened___set_generic_property_int64_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_int64_array("Dev1", "Dev.Timestamps", [100, 200])

    interpreter.set_generic_property_int64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timestamps", [100, 200]
    )


def test___session_opened___set_generic_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_string("Dev1", "Dev.Name", "NewName")

    interpreter.set_generic_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.Name", "NewName"
    )


def test___session_opened___set_generic_property_string_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_string_array("Dev1", "Dev.Labels", ["a", "b"])

    interpreter.set_generic_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Labels", ["a", "b"]
    )


def test___session_opened___set_generic_property_uint32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_uint32("Dev1", "Dev.Count", 255)

    interpreter.set_generic_property_uint32.assert_called_once_with(
        session_handle, "Dev1", "Dev.Count", 255
    )


def test___session_opened___set_generic_property_uint32_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_uint32_array("Dev1", "Dev.Counts", [10, 20])

    interpreter.set_generic_property_uint32_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Counts", [10, 20]
    )


def test___session_opened___set_generic_property_uint64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_uint64("Dev1", "Dev.LargeCount", 18446744073709551615)

    interpreter.set_generic_property_uint64.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCount", 18446744073709551615
    )


def test___session_opened___set_generic_property_uint64_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_uint64_array("Dev1", "Dev.LargeCounts", [111, 222])

    interpreter.set_generic_property_uint64_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.LargeCounts", [111, 222]
    )


def test___session_opened___execute_device_command___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.execute_device_command("Dev1", "Reset", 10.0)

    interpreter.execute_device_command.assert_called_once_with(
        session_handle, "Dev1", "Reset", 10.0
    )


def test___session_opened___execute_physical_channel_command___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.execute_physical_channel_command("Dev1/phys0", "Calibrate", 5.0)

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


def test___session_opened___read_register_uint8___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.read_register_uint8.return_value = 0xFF
    session_handle = session._session_handle

    result = session.read_register_uint8("Dev1", 0x00)

    interpreter.read_register_uint8.assert_called_once_with(session_handle, "Dev1", 0x00)
    assert result == 0xFF


def test___session_opened___read_register_uint16___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.read_register_uint16.return_value = 0xFFFF
    session_handle = session._session_handle

    result = session.read_register_uint16("Dev1", 0x02)

    interpreter.read_register_uint16.assert_called_once_with(session_handle, "Dev1", 0x02)
    assert result == 0xFFFF


def test___session_opened___read_register_uint32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.read_register_uint32.return_value = 0xDEADBEEF
    session_handle = session._session_handle

    result = session.read_register_uint32("Dev1", 0x04)

    interpreter.read_register_uint32.assert_called_once_with(session_handle, "Dev1", 0x04)
    assert result == 0xDEADBEEF


def test___session_opened___read_register_uint64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.read_register_uint64.return_value = 0xDEADBEEFCAFEBABE
    session_handle = session._session_handle

    result = session.read_register_uint64("Dev1", 0x08)

    interpreter.read_register_uint64.assert_called_once_with(session_handle, "Dev1", 0x08)
    assert result == 0xDEADBEEFCAFEBABE


def test___session_opened___write_register_uint8___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.write_register_uint8("Dev1", 0x00, 0xAB)

    interpreter.write_register_uint8.assert_called_once_with(session_handle, "Dev1", 0x00, 0xAB)


def test___session_opened___write_register_uint16___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.write_register_uint16("Dev1", 0x02, 0xABCD)

    interpreter.write_register_uint16.assert_called_once_with(session_handle, "Dev1", 0x02, 0xABCD)


def test___session_opened___write_register_uint32___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.write_register_uint32("Dev1", 0x04, 0xDEADBEEF)

    interpreter.write_register_uint32.assert_called_once_with(
        session_handle, "Dev1", 0x04, 0xDEADBEEF
    )


def test___session_opened___write_register_uint64___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.write_register_uint64("Dev1", 0x08, 0xDEADBEEFCAFEBABE)

    interpreter.write_register_uint64.assert_called_once_with(
        session_handle, "Dev1", 0x08, 0xDEADBEEFCAFEBABE
    )


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

    interpreter.commit_nvmem_generic.assert_called_once_with(
        session_handle, "$DefaultDevices"
    )


def test___session_opened___get_linear_scaling_parameters___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_linear_scaling_parameters.return_value = (2.0, 0.5)
    session_handle = session._session_handle

    result = session.get_linear_scaling_parameters("Dev1/phys0")

    interpreter.get_linear_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0"
    )
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

    interpreter.get_table_scaling_parameters.assert_called_once_with(
        session_handle, "Dev1/phys0"
    )
    assert result == ([0.0, 1.0], [0.0, 10.0], 0)


def test___session_opened___get_user_defined_scaling_parameters___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_user_defined_scaling_parameters.return_value = (["gain", "offset"], [2.0, 0.5])
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

    session.set_user_defined_scaling_equation(
        "Dev1/phys0", "gain * x + offset", "SN001", "pass"
    )

    interpreter.set_user_defined_scaling_equation.assert_called_once_with(
        session_handle, "Dev1/phys0", "gain * x + offset", "SN001", "pass"
    )


def test___session_opened___commit_scaling_for_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.commit_scaling_for_devices("Dev1")

    interpreter.commit_scaling_for_devices.assert_called_once_with(session_handle, "Dev1")