from __future__ import annotations

from unittest.mock import Mock

from nislsc import Library, Session
from nislsc.constants import ReservationAccess
from tests.unit._session_utils import (
    expect_initialize_library,
    expect_initialize_session_with_devices,
    expect_initialize_session_with_nvmem_areas,
    expect_initialize_session_with_physical_channels,
    expect_initialize_session_without_resources,
)


def test___initialize_session_with_devices___session_handle_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)

    with Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._session_handle == 100
        interpreter.initialize_session_with_devices.assert_called_once()


def test___initialize_session_with_devices_with_library___does_not_own_library(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter)

    with Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert not session._owns_library


def test___initialize_session_with_devices_no_library___creates_and_owns_library(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_devices(interpreter)

    with Session.initialize_session_with_devices(
        None, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._owns_library
        assert session._library is not None


def test___initialize_session_with_devices___passes_args_to_interpreter(
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


def test___initialize_session_with_nvmem_areas___session_handle_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_nvmem_areas(interpreter, 200)

    with Session.initialize_session_with_nvmem_areas(
        library, "Area1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._session_handle == 200
        interpreter.initialize_session_with_nvmem_areas.assert_called_once()


def test___initialize_session_with_nvmem_areas_no_library___creates_and_owns_library(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_nvmem_areas(interpreter)

    with Session.initialize_session_with_nvmem_areas(
        None, "Area1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._owns_library


def test___initialize_session_with_physical_channels___session_handle_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_physical_channels(interpreter, 300)

    with Session.initialize_session_with_physical_channels(
        library, "Dev1/phys0", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._session_handle == 300
        interpreter.initialize_session_with_physical_channels.assert_called_once()


def test___initialize_session_with_physical_channels_no_library___creates_and_owns_library(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_with_physical_channels(interpreter)

    with Session.initialize_session_with_physical_channels(
        None, "Dev1/phys0", -1.0, ReservationAccess.NONE, "", -1.0
    ) as session:
        assert session._owns_library


def test___initialize_session_without_resources___session_handle_set(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_without_resources(interpreter, 400)

    with Session.initialize_session_without_resources(library) as session:
        assert session._session_handle == 400
        interpreter.initialize_session_without_resources.assert_called_once()


def test___initialize_session_without_resources_no_library___creates_and_owns_library(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)
    expect_initialize_session_without_resources(interpreter)

    with Session.initialize_session_without_resources(None) as session:
        assert session._owns_library


def test___close___close_session_called_with_handle(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.close()

    interpreter.close_session.assert_called_once_with(session_handle)
    assert session._session_handle == 0


def test___close_twice___close_session_called_once(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.close()
    session.close()

    interpreter.close_session.assert_called_once_with(session_handle)


def test___context_manager___close_session_called_on_exit(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)

    with Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ):
        interpreter.close_session.assert_not_called()

    interpreter.close_session.assert_called_once_with(100)


def test___close_owns_library___also_finalizes_library(
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


def test___close_does_not_own_library___does_not_finalize_library(
    interpreter: Mock, library: Library
) -> None:
    expect_initialize_session_with_devices(interpreter, 100)
    session = Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    )

    session.close()

    interpreter.finalize_library.assert_not_called()


def test___abort_session___interpreter_called(interpreter: Mock, session: Session) -> None:
    session_handle = session._session_handle

    session.abort_session()

    interpreter.abort_session.assert_called_once_with(session_handle)


def test___log_in___interpreter_called_with_args(interpreter: Mock, session: Session) -> None:
    session_handle = session._session_handle

    session.log_in("Chassis1", "admin", "secret", 10.0, False)

    interpreter.log_in.assert_called_once_with(
        session_handle, "Chassis1", "admin", "secret", 10.0, False
    )


def test___log_out___interpreter_called_with_chassis_name(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.log_out("Chassis1")

    interpreter.log_out.assert_called_once_with(session_handle, "Chassis1")


def test___connect_to_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.connect_to_devices("Dev1", 10.0)

    interpreter.connect_to_devices.assert_called_once_with(session_handle, "Dev1", 10.0)


def test___disconnect_from_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.disconnect_from_devices("Dev1")

    interpreter.disconnect_from_devices.assert_called_once_with(session_handle, "Dev1")


def test___connect_to_chassis_by_address___returns_chassis_name(
    interpreter: Mock, session: Session
) -> None:
    interpreter.connect_to_chassis_by_address.return_value = "Chassis1"
    session_handle = session._session_handle

    result = session.connect_to_chassis_by_address("192.168.1.1", "admin", "pass", 10.0)

    interpreter.connect_to_chassis_by_address.assert_called_once_with(
        session_handle, "192.168.1.1", "admin", "pass", 10.0
    )
    assert result == "Chassis1"


def test___reserve_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.reserve_devices("Dev1", ReservationAccess.READ_WRITE, "MyGroup", 30.0)

    interpreter.reserve_devices.assert_called_once_with(
        session_handle, "Dev1", ReservationAccess.READ_WRITE, "MyGroup", 30.0
    )


def test___unreserve_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.unreserve_devices("Dev1")

    interpreter.unreserve_devices.assert_called_once_with(session_handle, "Dev1")


def test___reset_devices___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.reset_devices("Dev1")

    interpreter.reset_devices.assert_called_once_with(session_handle, "Dev1")


def test___rename_device___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.rename_device("Dev1", "Dev2")

    interpreter.rename_device.assert_called_once_with(session_handle, "Dev1", "Dev2")


def test___add_network_chassis___returns_chassis_name(
    interpreter: Mock, session: Session
) -> None:
    interpreter.add_network_chassis.return_value = "Chassis1"
    session_handle = session._session_handle

    result = session.add_network_chassis("192.168.1.1", "admin", "pass", 10.0)

    interpreter.add_network_chassis.assert_called_once_with(
        session_handle, "192.168.1.1", "admin", "pass", 10.0
    )
    assert result == "Chassis1"


def test___remove_chassis___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.remove_chassis("Chassis1")

    interpreter.remove_chassis.assert_called_once_with(session_handle, "Chassis1")


def test___update_system_configuration_file___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.update_system_configuration_file("Chassis1", 5.0)

    interpreter.update_system_configuration_file.assert_called_once_with(
        session_handle, "Chassis1", 5.0
    )


def test___get_device_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_bool.return_value = True
    session_handle = session._session_handle

    result = session.get_device_property_bool("Dev1", "Dev.IsPresent")

    interpreter.get_device_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.IsPresent"
    )
    assert result is True


def test___get_device_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_double.return_value = 3.14
    session_handle = session._session_handle

    result = session.get_device_property_double("Dev1", "Dev.Temperature")

    interpreter.get_device_property_double.assert_called_once_with(
        session_handle, "Dev1", "Dev.Temperature"
    )
    assert result == 3.14


def test___get_device_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_string.return_value = "SLSC-12201"
    session_handle = session._session_handle

    result = session.get_device_property_string("Dev1", "Dev.ProductName")

    interpreter.get_device_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.ProductName"
    )
    assert result == "SLSC-12201"


def test___get_device_property_int32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_int32.return_value = 7
    session_handle = session._session_handle

    result = session.get_device_property_int32("Dev1", "Dev.NumSlots")

    interpreter.get_device_property_int32.assert_called_once_with(
        session_handle, "Dev1", "Dev.NumSlots"
    )
    assert result == 7


def test___get_device_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_device_property_string_array.return_value = ["Mod1", "Mod2"]
    session_handle = session._session_handle

    result = session.get_device_property_string_array("Dev1", "Dev.Modules")

    interpreter.get_device_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Modules"
    )
    assert result == ["Mod1", "Mod2"]


def test___set_device_property_bool___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_bool("Dev1", "Dev.Enabled", True)

    interpreter.set_device_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.Enabled", True
    )


def test___set_device_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_string("Dev1", "Dev.Name", "NewName")

    interpreter.set_device_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.Name", "NewName"
    )


def test___set_device_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_device_property_double("Dev1", "Dev.Timeout", 5.0)

    interpreter.set_device_property_double.assert_called_once_with(
        session_handle, "Dev1", "Dev.Timeout", 5.0
    )


def test___get_physical_channel_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_bool.return_value = False
    session_handle = session._session_handle

    result = session.get_physical_channel_property_bool("Dev1/phys0", "PhysChan.IsActive")

    interpreter.get_physical_channel_property_bool.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.IsActive"
    )
    assert result is False


def test___get_physical_channel_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_string.return_value = "load0"
    session_handle = session._session_handle

    result = session.get_physical_channel_property_string("Dev1/phys0", "PhysChan.Name")

    interpreter.get_physical_channel_property_string.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Name"
    )
    assert result == "load0"


def test___set_physical_channel_property_bool___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_bool("Dev1/phys0", "PhysChan.Enabled", True)

    interpreter.set_physical_channel_property_bool.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Enabled", True
    )


def test___get_physical_channel_property_int32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_physical_channel_property_int32.return_value = 4
    session_handle = session._session_handle

    result = session.get_physical_channel_property_int32("Dev1/phys0", "PhysChan.Index")

    interpreter.get_physical_channel_property_int32.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Index"
    )
    assert result == 4


def test___get_physical_channel_property_string_array___returns_list(
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


def test___set_physical_channel_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_physical_channel_property_string("Dev1/phys0", "PhysChan.Label", "MyLabel")

    interpreter.set_physical_channel_property_string.assert_called_once_with(
        session_handle, "Dev1/phys0", "PhysChan.Label", "MyLabel"
    )


def test___get_nvmem_area_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_bool.return_value = True
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_bool("Area1", "NVMem.IsWritable")

    interpreter.get_nvmem_area_property_bool.assert_called_once_with(
        session_handle, "Area1", "NVMem.IsWritable"
    )
    assert result is True


def test___get_nvmem_area_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_string.return_value = "Area1"
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_string("Area1", "NVMem.Name")

    interpreter.get_nvmem_area_property_string.assert_called_once_with(
        session_handle, "Area1", "NVMem.Name"
    )
    assert result == "Area1"


def test___get_nvmem_area_property_uint32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_uint32.return_value = 512
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_uint32("Area1", "NVMem.Size")

    interpreter.get_nvmem_area_property_uint32.assert_called_once_with(
        session_handle, "Area1", "NVMem.Size"
    )
    assert result == 512


def test___get_nvmem_area_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_nvmem_area_property_string_array.return_value = ["Area1", "Area2"]
    session_handle = session._session_handle

    result = session.get_nvmem_area_property_string_array("Area1", "NVMem.Areas")

    interpreter.get_nvmem_area_property_string_array.assert_called_once_with(
        session_handle, "Area1", "NVMem.Areas"
    )
    assert result == ["Area1", "Area2"]


def test___get_session_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_session_property_double.return_value = 10.0
    session_handle = session._session_handle

    result = session.get_session_property_double("Session.Timeout")

    interpreter.get_session_property_double.assert_called_once_with(
        session_handle, "Session.Timeout"
    )
    assert result == 10.0


def test___get_session_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_session_property_string.return_value = "Dev1"
    session_handle = session._session_handle

    result = session.get_session_property_string("Session.DefaultDevices")

    interpreter.get_session_property_string.assert_called_once_with(
        session_handle, "Session.DefaultDevices"
    )
    assert result == "Dev1"


def test___get_session_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_session_property_string_array.return_value = ["Dev1", "Dev2"]
    session_handle = session._session_handle

    result = session.get_session_property_string_array("Session.Devices")

    interpreter.get_session_property_string_array.assert_called_once_with(
        session_handle, "Session.Devices"
    )
    assert result == ["Dev1", "Dev2"]


def test___set_session_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_session_property_double("Session.Timeout", 30.0)

    interpreter.set_session_property_double.assert_called_once_with(
        session_handle, "Session.Timeout", 30.0
    )


def test___set_session_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_session_property_string("Session.DefaultDevices", "Dev1")

    interpreter.set_session_property_string.assert_called_once_with(
        session_handle, "Session.DefaultDevices", "Dev1"
    )


def test___set_session_property_string_array___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_session_property_string_array("Session.Devices", ["Dev1", "Dev2"])

    interpreter.set_session_property_string_array.assert_called_once_with(
        session_handle, "Session.Devices", ["Dev1", "Dev2"]
    )


def test___get_system_property_double___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_system_property_double.return_value = 1.5
    session_handle = session._session_handle

    result = session.get_system_property_double("System.Version")

    interpreter.get_system_property_double.assert_called_once_with(
        session_handle, "System.Version"
    )
    assert result == 1.5


def test___get_system_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_system_property_string_array.return_value = ["Dev1", "Chassis1"]
    session_handle = session._session_handle

    result = session.get_system_property_string_array("System.Devices")

    interpreter.get_system_property_string_array.assert_called_once_with(
        session_handle, "System.Devices"
    )
    assert result == ["Dev1", "Chassis1"]


def test___get_system_property_uint64___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_system_property_uint64.return_value = 12345678
    session_handle = session._session_handle

    result = session.get_system_property_uint64("System.Timestamp")

    interpreter.get_system_property_uint64.assert_called_once_with(
        session_handle, "System.Timestamp"
    )
    assert result == 12345678


def test___set_system_property_double___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_system_property_double("System.Timeout", 5.0)

    interpreter.set_system_property_double.assert_called_once_with(
        session_handle, "System.Timeout", 5.0
    )


def test___get_generic_property_bool___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_bool.return_value = False
    session_handle = session._session_handle

    result = session.get_generic_property_bool("Dev1", "Dev.IsPresent")

    interpreter.get_generic_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.IsPresent"
    )
    assert result is False


def test___get_generic_property_int32___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_int32.return_value = 3
    session_handle = session._session_handle

    result = session.get_generic_property_int32("Dev1", "Dev.NumSlots")

    interpreter.get_generic_property_int32.assert_called_once_with(
        session_handle, "Dev1", "Dev.NumSlots"
    )
    assert result == 3


def test___get_generic_property_string___returns_value(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_string.return_value = "SLSC-12201"
    session_handle = session._session_handle

    result = session.get_generic_property_string("Dev1", "Dev.ProductName")

    interpreter.get_generic_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.ProductName"
    )
    assert result == "SLSC-12201"


def test___get_generic_property_string_array___returns_list(
    interpreter: Mock, session: Session
) -> None:
    interpreter.get_generic_property_string_array.return_value = ["Mod1", "Mod2"]
    session_handle = session._session_handle

    result = session.get_generic_property_string_array("Dev1", "Dev.Modules")

    interpreter.get_generic_property_string_array.assert_called_once_with(
        session_handle, "Dev1", "Dev.Modules"
    )
    assert result == ["Mod1", "Mod2"]


def test___set_generic_property_bool___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_bool("Dev1", "Dev.Enabled", True)

    interpreter.set_generic_property_bool.assert_called_once_with(
        session_handle, "Dev1", "Dev.Enabled", True
    )


def test___set_generic_property_string___interpreter_called_with_args(
    interpreter: Mock, session: Session
) -> None:
    session_handle = session._session_handle

    session.set_generic_property_string("Dev1", "Dev.Name", "NewName")

    interpreter.set_generic_property_string.assert_called_once_with(
        session_handle, "Dev1", "Dev.Name", "NewName"
    )