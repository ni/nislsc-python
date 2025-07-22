from typing_extensions import Self

import warnings
from types import TracebackType

from nislsc.session._session import Session
from nislsc.error import SLSCResourceWarning

class Command():
    """
    Represent Command class for NI SLSC.
    """
    def __init__(self, session: Session, command_handle: int) -> None:
        """Initialize a Command instance.

        Args:
            session: Previously initialized Session instance
            command_handle: The command handle returned by the
                initialization function.
        """
        self._property_handle = property_handle
        self._session = session
        self._interpreter = session._interpreter

    def __enter__(self) -> Self:
        """Enter the runtime context.

        Returns:
            Self: The command object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the Command instance.
        
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
        Remind the user that the Command instance is not closed.
        """
        if self._command_handle is not None:
            warnings.warn(
                'Command was not closed before it was destructed. Resources on the'
                'Command may still be reserved.',
                SLSCResourceWarning
            )

    def close(self) -> None:
        """
        Close the command instance.
        """
        if self._command_handle is not None:
            self._interpreter.close_command(self._command_handle)
            self._command_handle = None

    @classmethod
    def open_device_command(cls, session: Session, device_name: str, command_name: str) -> Self:
        """Open a reference to a device command.
        
        This allows the application to programmatically get information about
        the command at run time.
        
        Args:
            session: Previously initialized Session instance.
            device_name: Device where the command is located, or a resource
                alias such as "$DefaultDevices".
            command_name: Name of command to open
        
        Returns:
            Self: New instance of CommandReference object.
        """
        session_handle = session._session_handle
        interpreter = session._interpreter
        command_handle = interpreter.open_device_command(session_handle, device_name, command_name)
        return cls(session, command_handle)

    @classmethod
    def open_physical_channel_command(cls, session: Session, physical_channel_names: str, command_name: str) -> Self:
        """Open a reference to a physical channel command.
        
        This allows the application to programmatically get information about
        the command at run time.
        
        Args:
            session: Previously initialized Session instance.
            physical_channel_names: Physical channel where the command is
                located, or a resource alias such as "$DefaultPhysChans".
            command_name: Name of command to open
        
        Returns:
            Self: New instance of CommandReference object.
        """
        session_handle = session._session_handle
        interpreter = session._interpreter
        command_handle = interpreter.open_physical_channel_command(session_handle, physical_channel_names, command_name)
        return cls(session, command_handle)

    @classmethod
    def open_generic_command(cls, session: Session, resource: str, command_name: str) -> Self:
        """Open a reference to a command.
        
        This allows the application to programmatically get information about
        the command at run time.
        
        Args:
            session: Previously initialized Session instance.
            resource: Resource where the command is located, or a resource alias
                such as "$DefaultDevices".
            command_name: Name of command to open
        
        Returns:
            Self: New instance of CommandReference object.
        """
        session_handle = session._session_handle
        interpreter = session._interpreter
        command_handle = interpreter.open_generic_command(session_handle, resource, command_name)
        return cls(session, command_handle)

    def close_command(self) -> None:
        """Close an open reference to a command.
        """
        self._interpreter.close_command(self._command_handle)

    def get_command_property_string(self, property_name: str) -> str:
        """Get the value of the specified command reflection property.
        
        Args:
            property_name: Name of command reflection property to get
        
        Returns:
            property_value: Value of property
        """
        property_value = self._interpreter.get_command_property_string(self._command_handle, property_name)
        return property_value

