from typing_extensions import Self

from nislsc._base_interpreter import BaseInterpreter
from types import TracebackType

class Property():
    """
    Represent Property class for NI SLSC.
    """

    def __init__(self, property_handle: int, interpreter: BaseInterpreter) -> None:
        """Initialize a Property instance.

        Args:
            property_handle: The property handle returned by the
                initialization function.
            interpreter: The interpreter instance used for
                communication.
        """
        self._property_handle = property_handle
        self._interpreter = interpreter

    def __enter__(self) -> Self:
        """Enter the runtime context related to this object.

        Returns:
            Self: The property object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the Property instance.

        Args:
            type: The exception type, if an exception was raised, otherwise 
                None.
            value: The exception value, if an exception was raised, otherwise
                None.
            traceback: The traceback, if an exception was raised, otherwise 
                None.
        """
        self.close()

    def __del__(self) -> None:
        """
        Remind the user that the Property instance is not closed.
        """
        if self._session_handle is not None:
            warnings.warn(
                'Property was not closed before it was destructed. Resources on the'
                'Property may still be reserved.',
                SLSCResourceWarning
            )

    def close(self) -> None:
        """
        Close the Property instance.
        """
        if self._property_handle is not None:
            self._interpreter.close_property(self._property_handle)
            self._property_handle = None

    def get_property_property_bool(self, property_name: str) -> bool:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get
        
        Returns:
            property_value: Value of property
        """
        return self._interpreter.get_property_property_bool(self._property_handle, property_name)

    def get_property_property_int32(self, property_name: str) -> int:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get
        
        Returns:
            property_value: Value of property
        """
        return self._interpreter.get_property_property_int32(self._property_handle, property_name)

    def get_property_property_int32_array(self, property_name: str) -> list[int]:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get
        
        Returns:
            property_value: Value of property
        """
        return self._interpreter.get_property_property_int32_array(self._property_handle, property_name)

    def get_property_property_string(self, property_name: str) -> str:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get
        
        Returns:
            property_value: Value of property
        """
        return self._interpreter.get_property_property_string(self._property_handle, property_name)

    def get_property_property_string_array(self, property_name: str) -> list[str]:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get
        
        Returns:
            property_value: Value of property
        """
        return self._interpreter.get_property_property_string_array(self._property_handle, property_name)

