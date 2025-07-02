from nislsc._base_interpreter import BaseInterpreter
from types import TracebackType

class Property():
    """Represents a property object for NI SLSC.

    This class manages the property handle and interpreter, and provides context
    management and resource cleanup for SLSC properties.
    """

    def __init__(self, property_handle: int, interpreter: BaseInterpreter) -> None:
        """Initializes a Property instance.

        Args:
            property_handle (int): The property handle returned by the initialization function.
            interpreter (BaseInterpreter): The interpreter instance used for communication.
        """
        self._property_handle = property_handle
        self._interpreter = interpreter

    def __enter__(self) -> "Property":
        """Enter the runtime context related to this object.

        Returns:
            Property: The property object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the property handle.

        Args:
            type (type[BaseException] | None): The exception type, if an exception was raised, otherwise None.
            value (BaseException | None): The exception value, if an exception was raised, otherwise None.
            traceback (TracebackType | None): The traceback, if an exception was raised, otherwise None.
        """
        self._interpreter.close_property(self._property_handle)
        self._property_handle = 0

    def __del__(self) -> None:
        """Destructor to ensure the property is closed when the object is deleted."""
        if self._property_handle != 0:
            self._interpreter.close_property(self._property_handle)

    def get_property_property_bool(self, property_name: str) -> bool:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name (str): Name of property reflection property to get
        
        Returns:
            property_value (bool): Value of property
        """
        return self._interpreter.get_property_property_bool(self._property_handle, property_name)

    def get_property_property_int32(self, property_name: str) -> int:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name (str): Name of property reflection property to get
        
        Returns:
            property_value (int): Value of property
        """
        return self._interpreter.get_property_property_int32(self._property_handle, property_name)

    def get_property_property_int32_array(self, property_name: str) -> list[int]:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name (str): Name of property reflection property to get
        
        Returns:
            property_value (list[int]): Value of property
        """
        return self._interpreter.get_property_property_int32_array(self._property_handle, property_name)

    def get_property_property_string(self, property_name: str) -> str:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name (str): Name of property reflection property to get
        
        Returns:
            property_value (str): Value of property
        """
        return self._interpreter.get_property_property_string(self._property_handle, property_name)

    def get_property_property_string_array(self, property_name: str) -> list[str]:
        """Gets the value of the specified property reflection property.
        
        Args:
            property_name (str): Name of property reflection property to get
        
        Returns:
            property_value (list[str]): Value of property
        """
        return self._interpreter.get_property_property_string_array(self._property_handle, property_name)

