from nislsc._library_interpreter import LibraryInterpreter
from nislsc.constants import Language

class Library():
    def __init__(self, version) -> None:
        self._interpreter = LibraryInterpreter()
        self._library_handle = self._interpreter.initialize_library(self._interpreter.get_library_version())
        self._language = Language.CURRENT_THREAD_LOCALE

    def __enter__(self) -> Library:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.finalize_library(self._library_handle)

    def __del__(self) -> None:
        if self._library_handle is not None:
            self._interpreter.finalize_library(self._library_handle)

    def get_extended_error_info(self, language: int) -> str:
        return self._interpreter.get_extended_error_info(self._library_handle, language)

    def get_error_description(self, status_code: int, language: int) -> str:
        return self._interpreter.get_error_description(self._library_handle, status_code, language)

    def initialize_session_with_devices(self, device_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int | None:
        return Session(self._interpreter.initialize_session_with_devices(self._library_handle, device_names, connection_timeout, reservation_access, reservation_group, reservation_timeout), self._interpreter)

    def initialize_session_with_nvmem_areas(self, nvmem_area_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int | None:
        return Session(self._interpreter.initialize_session_with_nvmem_areas(self._library_handle, nvmem_area_names, connection_timeout, reservation_access, reservation_group, reservation_timeout), self._interpreter)

    def initialize_session_with_physical_channels(self, physical_channel_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int | None:
        return Session(self._interpreter.initialize_session_with_physical_channels(self._library_handle, physical_channel_names, connection_timeout, reservation_access, reservation_group, reservation_timeout), self._interpreter)

    def initialize_session_without_resources(self) -> int | None:
        return Session(self._interpreter.initialize_session_without_resources(self._library_handle), self._interpreter)

