import abc
from nislsc.constants import Language

class BaseInterpreter(abc.ABC):

    @abc.abstractmethod
    def initialize_library(self, version: int) -> int:
        pass

    @abc.abstractmethod
    def finalize_library(self, library_handle: int) -> None:
        pass

    @abc.abstractmethod
    def get_library_version(self) -> int:
        pass

    @abc.abstractmethod
    def get_extended_error_info(self, library_handle: int, language: Language) -> str:
        pass

    @abc.abstractmethod
    def get_error_description(self, library_handle: int, status_code: int, language: Language) -> str:
        pass

    @abc.abstractmethod
    def flatten_names(self, names_in: list[str]) -> str:
        pass

    @abc.abstractmethod
    def unflatten_names(self, names_in: str) -> list[str]:
        pass

    @abc.abstractmethod
    def initialize_session_with_devices(self, library_handle: int, device_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int:
        pass

    @abc.abstractmethod
    def initialize_session_with_nvmem_areas(self, library_handle: int, nvmem_area_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int:
        pass

    @abc.abstractmethod
    def initialize_session_with_physical_channels(self, library_handle: int, physical_channel_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int:
        pass

    @abc.abstractmethod
    def initialize_session_without_resources(self, library_handle: int) -> int:
        pass

    @abc.abstractmethod
    def close_session(self, session_handle: int) -> None:
        pass

    @abc.abstractmethod
    def abort_session(self, session_handle: int) -> None:
        pass

    @abc.abstractmethod
    def log_in(self, session_handle: int, chassis_name: str, username: str, password: str, connection_timeout: float, save_credentials_to_disk: bool) -> None:
        pass

    @abc.abstractmethod
    def log_out(self, session_handle: int, chassis_name: str) -> None:
        pass

    @abc.abstractmethod
    def connect_to_devices(self, session_handle: int, device_names: str, connection_timeout: float) -> None:
        pass

    @abc.abstractmethod
    def disconnect_from_devices(self, session_handle: int, device_names: str) -> None:
        pass

    @abc.abstractmethod
    def connect_to_chassis_by_address(self, session_handle: int, address: str, username: str, password: str, connection_timeout: float) -> str:
        pass

    @abc.abstractmethod
    def reserve_devices(self, session_handle: int, device_names: str, reservation_access: int, reservation_group: str, reservation_timeout: float) -> None:
        pass

    @abc.abstractmethod
    def unreserve_devices(self, session_handle: int, device_names: str) -> None:
        pass

    @abc.abstractmethod
    def reset_devices(self, session_handle: int, device_names: str) -> None:
        pass

    @abc.abstractmethod
    def rename_device(self, session_handle: int, device_name: str, new_device_name: str) -> None:
        pass

    @abc.abstractmethod
    def update_system_configuration_file(self, session_handle: int, chassis_name: str, connection_timeout: float) -> None:
        pass

    @abc.abstractmethod
    def add_network_chassis(self, session_handle: int, address: str, username: str, password: str, connection_timeout: float) -> str:
        pass

    @abc.abstractmethod
    def remove_chassis(self, session_handle: int, chassis_name: str) -> None:
        pass

    @abc.abstractmethod
    def get_device_property_bool(self, session_handle: int, device_names: str, property_name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_device_property_bool_array(self, session_handle: int, device_names: str, property_name: str) -> list[bool]:
        pass

    @abc.abstractmethod
    def get_device_property_double(self, session_handle: int, device_names: str, property_name: str) -> float:
        pass

    @abc.abstractmethod
    def get_device_property_double_array(self, session_handle: int, device_names: str, property_name: str) -> list[float]:
        pass

    @abc.abstractmethod
    def get_device_property_int32(self, session_handle: int, device_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_device_property_int32_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_device_property_int64(self, session_handle: int, device_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_device_property_int64_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_device_property_string(self, session_handle: int, device_names: str, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_device_property_string_array(self, session_handle: int, device_names: str, property_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def get_device_property_uint32(self, session_handle: int, device_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_device_property_uint32_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_device_property_uint64(self, session_handle: int, device_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_device_property_uint64_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def set_device_property_bool(self, session_handle: int, device_names: str, property_name: str, property_value: bool) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_bool_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[bool]) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_double(self, session_handle: int, device_names: str, property_name: str, property_value: float) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_double_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[float]) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_int32(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_int32_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_int64(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_int64_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_string(self, session_handle: int, device_names: str, property_name: str, property_value: str) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_string_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[str]) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_uint32(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_uint32_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_uint64(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_device_property_uint64_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_bool(self, session_handle: int, physical_channel_names: str, property_name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_bool_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[bool]:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_double(self, session_handle: int, physical_channel_names: str, property_name: str) -> float:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_double_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[float]:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_int32(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_int32_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_int64(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_int64_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_string(self, session_handle: int, physical_channel_names: str, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_string_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_uint32(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_uint32_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_uint64(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_physical_channel_property_uint64_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_bool(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: bool) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_bool_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[bool]) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_double(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: float) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_double_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[float]) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_int32(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_int32_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_int64(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_int64_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_string(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: str) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_string_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[str]) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_uint32(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_uint32_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_uint64(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_physical_channel_property_uint64_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def commit_properties_for_devices(self, session_handle: int, device_names: str) -> None:
        pass

    @abc.abstractmethod
    def commit_properties_for_physical_channels(self, session_handle: int, physical_channel_names: str) -> None:
        pass

    @abc.abstractmethod
    def commit_properties_for_session(self, session_handle: int) -> None:
        pass

    @abc.abstractmethod
    def commit_properties_generic(self, session_handle: int, resources: str) -> None:
        pass

    @abc.abstractmethod
    def get_nvmem_area_property_bool(self, session_handle: int, nvmem_area_names: str, property_name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_nvmem_area_property_bool_array(self, session_handle: int, nvmem_area_names: str, property_name: str) -> list[bool]:
        pass

    @abc.abstractmethod
    def get_nvmem_area_property_string(self, session_handle: int, nvmem_area_names: str, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_nvmem_area_property_string_array(self, session_handle: int, nvmem_area_names: str, property_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def get_nvmem_area_property_uint32(self, session_handle: int, nvmem_area_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_nvmem_area_property_uint32_array(self, session_handle: int, nvmem_area_names: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_session_property_double(self, session_handle: int, property_name: str) -> float:
        pass

    @abc.abstractmethod
    def get_session_property_string(self, session_handle: int, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_session_property_string_array(self, session_handle: int, property_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def set_session_property_double(self, session_handle: int, property_name: str, property_value: float) -> None:
        pass

    @abc.abstractmethod
    def set_session_property_string(self, session_handle: int, property_name: str, property_value: str) -> None:
        pass

    @abc.abstractmethod
    def set_session_property_string_array(self, session_handle: int, property_name: str, property_value: list[str]) -> None:
        pass

    @abc.abstractmethod
    def get_system_property_double(self, session_handle: int, property_name: str) -> float:
        pass

    @abc.abstractmethod
    def get_system_property_string_array(self, session_handle: int, property_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def get_system_property_uint64(self, session_handle: int, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def set_system_property_double(self, session_handle: int, property_name: str, property_value: float) -> None:
        pass

    @abc.abstractmethod
    def get_generic_property_bool(self, session_handle: int, resources: str, property_name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_generic_property_bool_array(self, session_handle: int, resources: str, property_name: str) -> list[bool]:
        pass

    @abc.abstractmethod
    def get_generic_property_double(self, session_handle: int, resources: str, property_name: str) -> float:
        pass

    @abc.abstractmethod
    def get_generic_property_double_array(self, session_handle: int, resources: str, property_name: str) -> list[float]:
        pass

    @abc.abstractmethod
    def get_generic_property_int32(self, session_handle: int, resources: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_generic_property_int32_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_generic_property_int64(self, session_handle: int, resources: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_generic_property_int64_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_generic_property_string(self, session_handle: int, resources: str, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_generic_property_string_array(self, session_handle: int, resources: str, property_name: str) -> list[str]:
        pass

    @abc.abstractmethod
    def get_generic_property_uint32(self, session_handle: int, resources: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_generic_property_uint32_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_generic_property_uint64(self, session_handle: int, resources: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_generic_property_uint64_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def set_generic_property_bool(self, session_handle: int, resources: str, property_name: str, property_value: bool) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_bool_array(self, session_handle: int, resources: str, property_name: str, property_value: list[bool]) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_double(self, session_handle: int, resources: str, property_name: str, property_value: float) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_double_array(self, session_handle: int, resources: str, property_name: str, property_value: list[float]) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_int32(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_int32_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_int64(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_int64_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_string(self, session_handle: int, resources: str, property_name: str, property_value: str) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_string_array(self, session_handle: int, resources: str, property_name: str, property_value: list[str]) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_uint32(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_uint32_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_uint64(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        pass

    @abc.abstractmethod
    def set_generic_property_uint64_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        pass

    @abc.abstractmethod
    def execute_device_command(self, session_handle: int, device_names: str, command_name: str, timeout: float) -> None:
        pass

    @abc.abstractmethod
    def execute_physical_channel_command(self, session_handle: int, physical_channel_names: str, command_name: str, timeout: float) -> None:
        pass

    @abc.abstractmethod
    def execute_generic_command(self, session_handle: int, resources: str, command_name: str, timeout: float) -> None:
        pass

    @abc.abstractmethod
    def read_register_uint8(self, session_handle: int, device_name: str, register_address: int) -> int:
        pass

    @abc.abstractmethod
    def read_register_uint16(self, session_handle: int, device_name: str, register_address: int) -> int:
        pass

    @abc.abstractmethod
    def read_register_uint32(self, session_handle: int, device_name: str, register_address: int) -> int:
        pass

    @abc.abstractmethod
    def read_register_uint64(self, session_handle: int, device_name: str, register_address: int) -> int:
        pass

    @abc.abstractmethod
    def write_register_uint8(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        pass

    @abc.abstractmethod
    def write_register_uint16(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        pass

    @abc.abstractmethod
    def write_register_uint32(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        pass

    @abc.abstractmethod
    def write_register_uint64(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        pass

    @abc.abstractmethod
    def get_nvmem_bytes(self, session_handle: int, nvmem_area: str, nvmem_address: int, num_byte: int) -> bytes:
        pass

    @abc.abstractmethod
    def set_nvmem_bytes(self, session_handle: int, nvmem_area: str, nvmem_address: int, bytes_data: bytes, serial_number: str, password: str) -> None:
        pass

    @abc.abstractmethod
    def commit_nvmem_areas(self, session_handle: int, nvmem_area_names: str) -> None:
        pass

    @abc.abstractmethod
    def commit_nvmem_for_devices(self, session_handle: int, device_names: str) -> None:
        pass

    @abc.abstractmethod
    def commit_nvmem_for_session(self, session_handle: int) -> None:
        pass

    @abc.abstractmethod
    def commit_nvmem_generic(self, session_handle: int, resources: str) -> None:
        pass

    @abc.abstractmethod
    def get_linear_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[float, float]:
        pass

    @abc.abstractmethod
    def get_polynomial_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[list[float], list[float]]:
        pass

    @abc.abstractmethod
    def get_table_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[list[float], list[float], int]:
        pass

    @abc.abstractmethod
    def get_user_defined_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[list[str], list[float]]:
        pass

    @abc.abstractmethod
    def get_user_defined_scaling_equation(self, session_handle: int, physical_channel_names: str) -> str:
        pass

    @abc.abstractmethod
    def set_linear_scaling_parameters(self, session_handle: int, physical_channel_names: str, slope: float, intercept: float, serial_number: str, password: str) -> None:
        pass

    @abc.abstractmethod
    def set_polynomial_scaling_parameters(self, session_handle: int, physical_channel_names: str, forward_coefficient: list[float], reverse_coefficient: list[float], serial_number: str, password: str) -> None:
        pass

    @abc.abstractmethod
    def set_table_scaling_parameters(self, session_handle: int, physical_channel_names: str, scaled_value: list[float], prescale_value: list[float], coercion: int, serial_number: str, password: str) -> None:
        pass

    @abc.abstractmethod
    def set_user_defined_scaling_parameters(self, session_handle: int, physical_channel_names: str, user_defined_parameter_name: list[str], user_defined_parameter_value: list[float], serial_number: str, password: str) -> None:
        pass

    @abc.abstractmethod
    def set_user_defined_scaling_equation(self, session_handle: int, physical_channel_names: str, user_defined_equation: str, serial_number: str, password: str) -> None:
        pass

    @abc.abstractmethod
    def commit_scaling_for_devices(self, session_handle: int, device_names: str) -> None:
        pass

    @abc.abstractmethod
    def open_device_command(self, session_handle: int, device_name: str, command_name: str) -> int:
        pass

    @abc.abstractmethod
    def open_physical_channel_command(self, session_handle: int, physical_channel_names: str, command_name: str) -> int:
        pass

    @abc.abstractmethod
    def open_generic_command(self, session_handle: int, resource: str, command_name: str) -> int:
        pass

    @abc.abstractmethod
    def close_command(self, command_handle: int) -> None:
        pass

    @abc.abstractmethod
    def get_command_property_string(self, command_handle: int, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def open_device_property(self, session_handle: int, device_name: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def open_physical_channel_property(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def open_driver_defined_property(self, session_handle: int, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def open_generic_property(self, session_handle: int, resource: str, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def close_property(self, property_handle: int) -> None:
        pass

    @abc.abstractmethod
    def get_property_property_bool(self, property_handle: int, property_name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_property_property_int32(self, property_handle: int, property_name: str) -> int:
        pass

    @abc.abstractmethod
    def get_property_property_int32_array(self, property_handle: int, property_name: str) -> list[int]:
        pass

    @abc.abstractmethod
    def get_property_property_string(self, property_handle: int, property_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_property_property_string_array(self, property_handle: int, property_name: str) -> list[str]:
        pass


