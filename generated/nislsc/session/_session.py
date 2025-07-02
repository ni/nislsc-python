from nislsc._library_interpreter import LibraryInterpreter
from nislsc.command._command import Command
from nislsc.property._property import Property

class Session():
    def __init__(self, session_handle: int, interpreter: LibraryInterpreter) -> None:
        self._session_handle = session_handle
        self._interpreter = interpreter

    def __enter__(self) -> Session:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.close_session(self._session_handle)

    def __del__(self) -> None:
        if self._session_handle is not None:
            self._interpreter.close_session(self._session_handle)

    def abort_session(self) -> None:
        return self._interpreter.abort_session(self._session_handle)

    def log_in(self, chassis_name: str, username: str, password: str, connection_timeout: float, save_credentials_to_disk: bool) -> None:
        return self._interpreter.log_in(self._session_handle, chassis_name, username, password, connection_timeout, save_credentials_to_disk)

    def log_out(self, chassis_name: str) -> None:
        return self._interpreter.log_out(self._session_handle, chassis_name)

    def connect_to_devices(self, device_names: str, connection_timeout: float) -> None:
        return self._interpreter.connect_to_devices(self._session_handle, device_names, connection_timeout)

    def disconnect_from_devices(self, device_names: str) -> None:
        return self._interpreter.disconnect_from_devices(self._session_handle, device_names)

    def connect_to_chassis_by_address(self, address: str, username: str, password: str, connection_timeout: float) -> str:
        return self._interpreter.connect_to_chassis_by_address(self._session_handle, address, username, password, connection_timeout)

    def reserve_devices(self, device_names: str, reservation_access: int, reservation_group: str, reservation_timeout: float) -> None:
        return self._interpreter.reserve_devices(self._session_handle, device_names, reservation_access, reservation_group, reservation_timeout)

    def unreserve_devices(self, device_names: str) -> None:
        return self._interpreter.unreserve_devices(self._session_handle, device_names)

    def reset_devices(self, device_names: str) -> None:
        return self._interpreter.reset_devices(self._session_handle, device_names)

    def rename_device(self, device_name: str, new_device_name: str) -> None:
        return self._interpreter.rename_device(self._session_handle, device_name, new_device_name)

    def update_system_configuration_file(self, chassis_name: str, connection_timeout: float) -> None:
        return self._interpreter.update_system_configuration_file(self._session_handle, chassis_name, connection_timeout)

    def add_network_chassis(self, address: str, username: str, password: str, connection_timeout: float) -> str:
        return self._interpreter.add_network_chassis(self._session_handle, address, username, password, connection_timeout)

    def remove_chassis(self, chassis_name: str) -> None:
        return self._interpreter.remove_chassis(self._session_handle, chassis_name)

    def get_device_property_bool(self, device_names: str, property_name: str) -> bool:
        return self._interpreter.get_device_property_bool(self._session_handle, device_names, property_name)

    def get_device_property_bool_array(self, device_names: str, property_name: str) -> list[bool]:
        return self._interpreter.get_device_property_bool_array(self._session_handle, device_names, property_name)

    def get_device_property_double(self, device_names: str, property_name: str) -> float:
        return self._interpreter.get_device_property_double(self._session_handle, device_names, property_name)

    def get_device_property_double_array(self, device_names: str, property_name: str) -> list[float]:
        return self._interpreter.get_device_property_double_array(self._session_handle, device_names, property_name)

    def get_device_property_int32(self, device_names: str, property_name: str) -> int:
        return self._interpreter.get_device_property_int32(self._session_handle, device_names, property_name)

    def get_device_property_int32_array(self, device_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_device_property_int32_array(self._session_handle, device_names, property_name)

    def get_device_property_int64(self, device_names: str, property_name: str) -> int:
        return self._interpreter.get_device_property_int64(self._session_handle, device_names, property_name)

    def get_device_property_int64_array(self, device_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_device_property_int64_array(self._session_handle, device_names, property_name)

    def get_device_property_string(self, device_names: str, property_name: str) -> str:
        return self._interpreter.get_device_property_string(self._session_handle, device_names, property_name)

    def get_device_property_string_array(self, device_names: str, property_name: str) -> list[str]:
        return self._interpreter.get_device_property_string_array(self._session_handle, device_names, property_name)

    def get_device_property_uint32(self, device_names: str, property_name: str) -> int:
        return self._interpreter.get_device_property_uint32(self._session_handle, device_names, property_name)

    def get_device_property_uint32_array(self, device_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_device_property_uint32_array(self._session_handle, device_names, property_name)

    def get_device_property_uint64(self, device_names: str, property_name: str) -> int:
        return self._interpreter.get_device_property_uint64(self._session_handle, device_names, property_name)

    def get_device_property_uint64_array(self, device_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_device_property_uint64_array(self._session_handle, device_names, property_name)

    def set_device_property_bool(self, device_names: str, property_name: str, property_value: bool) -> None:
        return self._interpreter.set_device_property_bool(self._session_handle, device_names, property_name, property_value)

    def set_device_property_bool_array(self, device_names: str, property_name: str, property_value: list[bool]) -> None:
        return self._interpreter.set_device_property_bool_array(self._session_handle, device_names, property_name, property_value)

    def set_device_property_double(self, device_names: str, property_name: str, property_value: float) -> None:
        return self._interpreter.set_device_property_double(self._session_handle, device_names, property_name, property_value)

    def set_device_property_double_array(self, device_names: str, property_name: str, property_value: list[float]) -> None:
        return self._interpreter.set_device_property_double_array(self._session_handle, device_names, property_name, property_value)

    def set_device_property_int32(self, device_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_device_property_int32(self._session_handle, device_names, property_name, property_value)

    def set_device_property_int32_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_device_property_int32_array(self._session_handle, device_names, property_name, property_value)

    def set_device_property_int64(self, device_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_device_property_int64(self._session_handle, device_names, property_name, property_value)

    def set_device_property_int64_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_device_property_int64_array(self._session_handle, device_names, property_name, property_value)

    def set_device_property_string(self, device_names: str, property_name: str, property_value: str) -> None:
        return self._interpreter.set_device_property_string(self._session_handle, device_names, property_name, property_value)

    def set_device_property_string_array(self, device_names: str, property_name: str, property_value: list[str]) -> None:
        return self._interpreter.set_device_property_string_array(self._session_handle, device_names, property_name, property_value)

    def set_device_property_uint32(self, device_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_device_property_uint32(self._session_handle, device_names, property_name, property_value)

    def set_device_property_uint32_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_device_property_uint32_array(self._session_handle, device_names, property_name, property_value)

    def set_device_property_uint64(self, device_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_device_property_uint64(self._session_handle, device_names, property_name, property_value)

    def set_device_property_uint64_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_device_property_uint64_array(self._session_handle, device_names, property_name, property_value)

    def get_physical_channel_property_bool(self, physical_channel_names: str, property_name: str) -> bool:
        return self._interpreter.get_physical_channel_property_bool(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_bool_array(self, physical_channel_names: str, property_name: str) -> list[bool]:
        return self._interpreter.get_physical_channel_property_bool_array(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_double(self, physical_channel_names: str, property_name: str) -> float:
        return self._interpreter.get_physical_channel_property_double(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_double_array(self, physical_channel_names: str, property_name: str) -> list[float]:
        return self._interpreter.get_physical_channel_property_double_array(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_int32(self, physical_channel_names: str, property_name: str) -> int:
        return self._interpreter.get_physical_channel_property_int32(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_int32_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_physical_channel_property_int32_array(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_int64(self, physical_channel_names: str, property_name: str) -> int:
        return self._interpreter.get_physical_channel_property_int64(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_int64_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_physical_channel_property_int64_array(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_string(self, physical_channel_names: str, property_name: str) -> str:
        return self._interpreter.get_physical_channel_property_string(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_string_array(self, physical_channel_names: str, property_name: str) -> list[str]:
        return self._interpreter.get_physical_channel_property_string_array(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_uint32(self, physical_channel_names: str, property_name: str) -> int:
        return self._interpreter.get_physical_channel_property_uint32(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_uint32_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_physical_channel_property_uint32_array(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_uint64(self, physical_channel_names: str, property_name: str) -> int:
        return self._interpreter.get_physical_channel_property_uint64(self._session_handle, physical_channel_names, property_name)

    def get_physical_channel_property_uint64_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_physical_channel_property_uint64_array(self._session_handle, physical_channel_names, property_name)

    def set_physical_channel_property_bool(self, physical_channel_names: str, property_name: str, property_value: bool) -> None:
        return self._interpreter.set_physical_channel_property_bool(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_bool_array(self, physical_channel_names: str, property_name: str, property_value: list[bool]) -> None:
        return self._interpreter.set_physical_channel_property_bool_array(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_double(self, physical_channel_names: str, property_name: str, property_value: float) -> None:
        return self._interpreter.set_physical_channel_property_double(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_double_array(self, physical_channel_names: str, property_name: str, property_value: list[float]) -> None:
        return self._interpreter.set_physical_channel_property_double_array(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_int32(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_physical_channel_property_int32(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_int32_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_physical_channel_property_int32_array(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_int64(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_physical_channel_property_int64(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_int64_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_physical_channel_property_int64_array(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_string(self, physical_channel_names: str, property_name: str, property_value: str) -> None:
        return self._interpreter.set_physical_channel_property_string(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_string_array(self, physical_channel_names: str, property_name: str, property_value: list[str]) -> None:
        return self._interpreter.set_physical_channel_property_string_array(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_uint32(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_physical_channel_property_uint32(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_uint32_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_physical_channel_property_uint32_array(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_uint64(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_physical_channel_property_uint64(self._session_handle, physical_channel_names, property_name, property_value)

    def set_physical_channel_property_uint64_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_physical_channel_property_uint64_array(self._session_handle, physical_channel_names, property_name, property_value)

    def commit_properties_for_devices(self, device_names: str) -> None:
        return self._interpreter.commit_properties_for_devices(self._session_handle, device_names)

    def commit_properties_for_physical_channels(self, physical_channel_names: str) -> None:
        return self._interpreter.commit_properties_for_physical_channels(self._session_handle, physical_channel_names)

    def commit_properties_for_session(self) -> None:
        return self._interpreter.commit_properties_for_session(self._session_handle)

    def commit_properties_generic(self, resources: str) -> None:
        return self._interpreter.commit_properties_generic(self._session_handle, resources)

    def get_nvmem_area_property_bool(self, nvmem_area_names: str, property_name: str) -> bool:
        return self._interpreter.get_nvmem_area_property_bool(self._session_handle, nvmem_area_names, property_name)

    def get_nvmem_area_property_bool_array(self, nvmem_area_names: str, property_name: str) -> list[bool]:
        return self._interpreter.get_nvmem_area_property_bool_array(self._session_handle, nvmem_area_names, property_name)

    def get_nvmem_area_property_string(self, nvmem_area_names: str, property_name: str) -> str:
        return self._interpreter.get_nvmem_area_property_string(self._session_handle, nvmem_area_names, property_name)

    def get_nvmem_area_property_string_array(self, nvmem_area_names: str, property_name: str) -> list[str]:
        return self._interpreter.get_nvmem_area_property_string_array(self._session_handle, nvmem_area_names, property_name)

    def get_nvmem_area_property_uint32(self, nvmem_area_names: str, property_name: str) -> int:
        return self._interpreter.get_nvmem_area_property_uint32(self._session_handle, nvmem_area_names, property_name)

    def get_nvmem_area_property_uint32_array(self, nvmem_area_names: str, property_name: str) -> list[int]:
        return self._interpreter.get_nvmem_area_property_uint32_array(self._session_handle, nvmem_area_names, property_name)

    def get_session_property_double(self, property_name: str) -> float:
        return self._interpreter.get_session_property_double(self._session_handle, property_name)

    def get_session_property_string(self, property_name: str) -> str:
        return self._interpreter.get_session_property_string(self._session_handle, property_name)

    def get_session_property_string_array(self, property_name: str) -> list[str]:
        return self._interpreter.get_session_property_string_array(self._session_handle, property_name)

    def set_session_property_double(self, property_name: str, property_value: float) -> None:
        return self._interpreter.set_session_property_double(self._session_handle, property_name, property_value)

    def set_session_property_string(self, property_name: str, property_value: str) -> None:
        return self._interpreter.set_session_property_string(self._session_handle, property_name, property_value)

    def set_session_property_string_array(self, property_name: str, property_value: list[str]) -> None:
        return self._interpreter.set_session_property_string_array(self._session_handle, property_name, property_value)

    def get_system_property_double(self, property_name: str) -> float:
        return self._interpreter.get_system_property_double(self._session_handle, property_name)

    def get_system_property_string_array(self, property_name: str) -> list[str]:
        return self._interpreter.get_system_property_string_array(self._session_handle, property_name)

    def get_system_property_uint64(self, property_name: str) -> int:
        return self._interpreter.get_system_property_uint64(self._session_handle, property_name)

    def set_system_property_double(self, property_name: str, property_value: float) -> None:
        return self._interpreter.set_system_property_double(self._session_handle, property_name, property_value)

    def get_generic_property_bool(self, resources: str, property_name: str) -> bool:
        return self._interpreter.get_generic_property_bool(self._session_handle, resources, property_name)

    def get_generic_property_bool_array(self, resources: str, property_name: str) -> list[bool]:
        return self._interpreter.get_generic_property_bool_array(self._session_handle, resources, property_name)

    def get_generic_property_double(self, resources: str, property_name: str) -> float:
        return self._interpreter.get_generic_property_double(self._session_handle, resources, property_name)

    def get_generic_property_double_array(self, resources: str, property_name: str) -> list[float]:
        return self._interpreter.get_generic_property_double_array(self._session_handle, resources, property_name)

    def get_generic_property_int32(self, resources: str, property_name: str) -> int:
        return self._interpreter.get_generic_property_int32(self._session_handle, resources, property_name)

    def get_generic_property_int32_array(self, resources: str, property_name: str) -> list[int]:
        return self._interpreter.get_generic_property_int32_array(self._session_handle, resources, property_name)

    def get_generic_property_int64(self, resources: str, property_name: str) -> int:
        return self._interpreter.get_generic_property_int64(self._session_handle, resources, property_name)

    def get_generic_property_int64_array(self, resources: str, property_name: str) -> list[int]:
        return self._interpreter.get_generic_property_int64_array(self._session_handle, resources, property_name)

    def get_generic_property_string(self, resources: str, property_name: str) -> str:
        return self._interpreter.get_generic_property_string(self._session_handle, resources, property_name)

    def get_generic_property_string_array(self, resources: str, property_name: str) -> list[str]:
        return self._interpreter.get_generic_property_string_array(self._session_handle, resources, property_name)

    def get_generic_property_uint32(self, resources: str, property_name: str) -> int:
        return self._interpreter.get_generic_property_uint32(self._session_handle, resources, property_name)

    def get_generic_property_uint32_array(self, resources: str, property_name: str) -> list[int]:
        return self._interpreter.get_generic_property_uint32_array(self._session_handle, resources, property_name)

    def get_generic_property_uint64(self, resources: str, property_name: str) -> int:
        return self._interpreter.get_generic_property_uint64(self._session_handle, resources, property_name)

    def get_generic_property_uint64_array(self, resources: str, property_name: str) -> list[int]:
        return self._interpreter.get_generic_property_uint64_array(self._session_handle, resources, property_name)

    def set_generic_property_bool(self, resources: str, property_name: str, property_value: bool) -> None:
        return self._interpreter.set_generic_property_bool(self._session_handle, resources, property_name, property_value)

    def set_generic_property_bool_array(self, resources: str, property_name: str, property_value: list[bool]) -> None:
        return self._interpreter.set_generic_property_bool_array(self._session_handle, resources, property_name, property_value)

    def set_generic_property_double(self, resources: str, property_name: str, property_value: float) -> None:
        return self._interpreter.set_generic_property_double(self._session_handle, resources, property_name, property_value)

    def set_generic_property_double_array(self, resources: str, property_name: str, property_value: list[float]) -> None:
        return self._interpreter.set_generic_property_double_array(self._session_handle, resources, property_name, property_value)

    def set_generic_property_int32(self, resources: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_generic_property_int32(self._session_handle, resources, property_name, property_value)

    def set_generic_property_int32_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_generic_property_int32_array(self._session_handle, resources, property_name, property_value)

    def set_generic_property_int64(self, resources: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_generic_property_int64(self._session_handle, resources, property_name, property_value)

    def set_generic_property_int64_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_generic_property_int64_array(self._session_handle, resources, property_name, property_value)

    def set_generic_property_string(self, resources: str, property_name: str, property_value: str) -> None:
        return self._interpreter.set_generic_property_string(self._session_handle, resources, property_name, property_value)

    def set_generic_property_string_array(self, resources: str, property_name: str, property_value: list[str]) -> None:
        return self._interpreter.set_generic_property_string_array(self._session_handle, resources, property_name, property_value)

    def set_generic_property_uint32(self, resources: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_generic_property_uint32(self._session_handle, resources, property_name, property_value)

    def set_generic_property_uint32_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_generic_property_uint32_array(self._session_handle, resources, property_name, property_value)

    def set_generic_property_uint64(self, resources: str, property_name: str, property_value: int) -> None:
        return self._interpreter.set_generic_property_uint64(self._session_handle, resources, property_name, property_value)

    def set_generic_property_uint64_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        return self._interpreter.set_generic_property_uint64_array(self._session_handle, resources, property_name, property_value)

    def execute_device_command(self, device_names: str, command_name: str, timeout: float) -> None:
        return self._interpreter.execute_device_command(self._session_handle, device_names, command_name, timeout)

    def execute_physical_channel_command(self, physical_channel_names: str, command_name: str, timeout: float) -> None:
        return self._interpreter.execute_physical_channel_command(self._session_handle, physical_channel_names, command_name, timeout)

    def execute_generic_command(self, resources: str, command_name: str, timeout: float) -> None:
        return self._interpreter.execute_generic_command(self._session_handle, resources, command_name, timeout)

    def read_register_uint8(self, device_name: str, register_address: int) -> int:
        return self._interpreter.read_register_uint8(self._session_handle, device_name, register_address)

    def read_register_uint16(self, device_name: str, register_address: int) -> int:
        return self._interpreter.read_register_uint16(self._session_handle, device_name, register_address)

    def read_register_uint32(self, device_name: str, register_address: int) -> int:
        return self._interpreter.read_register_uint32(self._session_handle, device_name, register_address)

    def read_register_uint64(self, device_name: str, register_address: int) -> int:
        return self._interpreter.read_register_uint64(self._session_handle, device_name, register_address)

    def write_register_uint8(self, device_name: str, register_address: int, data: int) -> None:
        return self._interpreter.write_register_uint8(self._session_handle, device_name, register_address, data)

    def write_register_uint16(self, device_name: str, register_address: int, data: int) -> None:
        return self._interpreter.write_register_uint16(self._session_handle, device_name, register_address, data)

    def write_register_uint32(self, device_name: str, register_address: int, data: int) -> None:
        return self._interpreter.write_register_uint32(self._session_handle, device_name, register_address, data)

    def write_register_uint64(self, device_name: str, register_address: int, data: int) -> None:
        return self._interpreter.write_register_uint64(self._session_handle, device_name, register_address, data)

    def get_nvmem_bytes(self, nvmem_area: str, nvmem_address: int, num_byte: int) -> bytes:
        return self._interpreter.get_nvmem_bytes(self._session_handle, nvmem_area, nvmem_address, num_byte)

    def set_nvmem_bytes(self, nvmem_area: str, nvmem_address: int, bytes_data: bytes, serial_number: str, password: str) -> None:
        return self._interpreter.set_nvmem_bytes(self._session_handle, nvmem_area, nvmem_address, bytes_data, serial_number, password)

    def commit_nvmem_areas(self, nvmem_area_names: str) -> None:
        return self._interpreter.commit_nvmem_areas(self._session_handle, nvmem_area_names)

    def commit_nvmem_for_devices(self, device_names: str) -> None:
        return self._interpreter.commit_nvmem_for_devices(self._session_handle, device_names)

    def commit_nvmem_for_session(self) -> None:
        return self._interpreter.commit_nvmem_for_session(self._session_handle)

    def commit_nvmem_generic(self, resources: str) -> None:
        return self._interpreter.commit_nvmem_generic(self._session_handle, resources)

    def get_linear_scaling_parameters(self, physical_channel_names: str) -> tuple[float, float]:
        return self._interpreter.get_linear_scaling_parameters(self._session_handle, physical_channel_names)

    def get_polynomial_scaling_parameters(self, physical_channel_names: str) -> tuple[list[float], list[float]]:
        return self._interpreter.get_polynomial_scaling_parameters(self._session_handle, physical_channel_names)

    def get_table_scaling_parameters(self, physical_channel_names: str) -> tuple[list[float], list[float], int]:
        return self._interpreter.get_table_scaling_parameters(self._session_handle, physical_channel_names)

    def get_user_defined_scaling_parameters(self, physical_channel_names: str) -> tuple[list[str], list[float]]:
        return self._interpreter.get_user_defined_scaling_parameters(self._session_handle, physical_channel_names)

    def get_user_defined_scaling_equation(self, physical_channel_names: str) -> str:
        return self._interpreter.get_user_defined_scaling_equation(self._session_handle, physical_channel_names)

    def set_linear_scaling_parameters(self, physical_channel_names: str, slope: float, intercept: float, serial_number: str, password: str) -> None:
        return self._interpreter.set_linear_scaling_parameters(self._session_handle, physical_channel_names, slope, intercept, serial_number, password)

    def set_polynomial_scaling_parameters(self, physical_channel_names: str, forward_coefficient: list[float], reverse_coefficient: list[float], serial_number: str, password: str) -> None:
        return self._interpreter.set_polynomial_scaling_parameters(self._session_handle, physical_channel_names, forward_coefficient, reverse_coefficient, serial_number, password)

    def set_table_scaling_parameters(self, physical_channel_names: str, scaled_value: list[float], prescale_value: list[float], coercion: int, serial_number: str, password: str) -> None:
        return self._interpreter.set_table_scaling_parameters(self._session_handle, physical_channel_names, scaled_value, prescale_value, coercion, serial_number, password)

    def set_user_defined_scaling_parameters(self, physical_channel_names: str, user_defined_parameter_name: list[str], user_defined_parameter_value: list[float], serial_number: str, password: str) -> None:
        return self._interpreter.set_user_defined_scaling_parameters(self._session_handle, physical_channel_names, user_defined_parameter_name, user_defined_parameter_value, serial_number, password)

    def set_user_defined_scaling_equation(self, physical_channel_names: str, user_defined_equation: str, serial_number: str, password: str) -> None:
        return self._interpreter.set_user_defined_scaling_equation(self._session_handle, physical_channel_names, user_defined_equation, serial_number, password)

    def commit_scaling_for_devices(self, device_names: str) -> None:
        return self._interpreter.commit_scaling_for_devices(self._session_handle, device_names)

    def open_device_command(self, device_name: str, command_name: str) -> Command:
        return Command(self._interpreter.open_device_command(self._session_handle, device_name, command_name), self._interpreter)

    def open_physical_channel_command(self, physical_channel_names: str, command_name: str) -> Command:
        return Command(self._interpreter.open_physical_channel_command(self._session_handle, physical_channel_names, command_name), self._interpreter)

    def open_generic_command(self, resource: str, command_name: str) -> Command:
        return Command(self._interpreter.open_generic_command(self._session_handle, resource, command_name), self._interpreter)

    def open_device_property(self, device_name: str, property_name: str) -> Property:
        return Property(self._interpreter.open_device_property(self._session_handle, device_name, property_name), self._interpreter)

    def open_physical_channel_property(self, physical_channel_names: str, property_name: str) -> Property:
        return Property(self._interpreter.open_physical_channel_property(self._session_handle, physical_channel_names, property_name), self._interpreter)

    def open_driver_defined_property(self, property_name: str) -> Property:
        return Property(self._interpreter.open_driver_defined_property(self._session_handle, property_name), self._interpreter)

    def open_generic_property(self, resource: str, property_name: str) -> Property:
        return Property(self._interpreter.open_generic_property(self._session_handle, resource, property_name), self._interpreter)

