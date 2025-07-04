from nislsc._base_interpreter import BaseInterpreter
from types import TracebackType

class Command():
    """Represents a command object for NI SLSC.

    This class manages the command handle and interpreter, and provides 
    context management and resource cleanup for SLSC commands.
    """
    def __init__(self, command_handle: int, interpreter: BaseInterpreter) -> None:
        """Initializes a Command instance.

        Args:
            command_handle (int): The command handle returned by the
                initialization function.
            interpreter (BaseInterpreter): The interpreter instance used for
                communication.
        """
        self._command_handle = command_handle
        self._interpreter = interpreter

    def __enter__(self) -> "Command":
        """Enter the runtime context related to this object.

        Returns:
            Command: The command object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the command handle.
        
        Args:
            type (type[BaseException] | None): The exception type, if an
                exception was raised, otherwise None.
            value (BaseException | None): The exception value, if an exception
                was raised, otherwise None.
            traceback (TracebackType | None): The traceback, if an exception was
                raised, otherwise None.
        """
        self._interpreter.close_command(self._command_handle)
        self._command_handle = 0

    def __del__(self) -> None:
        """Destructor to ensure the command is closed when the object is
        deleted.
        """
        if self._command_handle != 0:
            self._interpreter.close_command(self._command_handle)

    def get_command_property_string(self, property_name: str) -> str:
        """Gets the value of the specified command reflection property.
        
        Args:
            property_name (str): Name of command reflection property to get
        
        Returns:
            property_value (str): Value of property
        """
        return self._interpreter.get_command_property_string(self._command_handle, property_name)

