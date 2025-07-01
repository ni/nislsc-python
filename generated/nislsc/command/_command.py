from nislsc._library_interpreter import LibraryInterpreter

class Command():
    def __init__(self, command_handle: int, interpreter: LibraryInterpreter) -> None:
        self._command_handle = command_handle
        self._interpreter = interpreter

    def __enter__(self) -> Command:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.close_command(self._command_handle)

    def __del__(self) -> None:
        if self._command_handle is not None:
            self._interpreter.close_command(self._command_handle)

    def get_command_property_string(self, property_name: str) -> str:
        return self._interpreter.get_command_property_string(self._command_handle, property_name)

