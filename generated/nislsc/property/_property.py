from nislsc._library_interpreter import LibraryInterpreter

class Property():
    def __init__(self, property_handle: int, interpreter: LibraryInterpreter) -> None:
        self._property_handle = property_handle
        self._interpreter = interpreter

    def __enter__(self) -> Property:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.close_property(self._property_handle)

    def __del__(self) -> None:
        if self._property_handle is not None:
            self._interpreter.close_property(self._property_handle)

    def get_property_property_bool(self, property_name: str) -> bool:
        return self._interpreter.get_property_property_bool(self._property_handle, property_name)

    def get_property_property_int32(self, property_name: str) -> int:
        return self._interpreter.get_property_property_int32(self._property_handle, property_name)

    def get_property_property_int32_array(self, property_name: str) -> list[int]:
        return self._interpreter.get_property_property_int32_array(self._property_handle, property_name)

    def get_property_property_string(self, property_name: str) -> str:
        return self._interpreter.get_property_property_string(self._property_handle, property_name)

    def get_property_property_string_array(self, property_name: str) -> list[str]:
        return self._interpreter.get_property_property_string_array(self._property_handle, property_name)

