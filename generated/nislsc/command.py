"""Open and execute SLSC device and physical channel commands.

This module provides a Command class for managing SLSC command
references that allow access to device and physical channel commands for
execution and introspection.
"""

from __future__ import annotations
import warnings
from types import TracebackType

from typing_extensions import Self

from nislsc.constants import Language
from nislsc.error import SLSCError, SLSCWarning
from nislsc.session import Session



class Command:
    """Execute and manage SLSC device and physical channel commands.
    
    Create command handles to execute device operations, retrieve command
    information, and perform command introspection. Use this class to run
    commands on SLSC hardware and access command metadata.
    """

    def __init__(self, session: Session, command_handle: int) -> None:
        """Create a Command instance.

        Args:
            session: Previously initialized Session instance
            command_handle: The command handle returned by the
                initialization function.
        """
        self._command_handle = command_handle
        self._session = session
        self._interpreter = session._interpreter

    def __enter__(self) -> Self:
        """Enter the runtime context.

        Returns:
            The command object itself.
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

    def close(self) -> None:
        """Close the command instance."""
        if self._command_handle != 0:
            self._interpreter.close_command(self._command_handle)
            self._command_handle = 0

    def _get_extended_error_info(self, language: Language = Language.UNDEFINED) -> str:
        """Return extended error information for the last error that occurred on
        the specified library handle.
        
        Args:
            language: Language to return error information in.
        
        Returns:
            Extended error info text.
        """
        language = self._session._library.language if language == Language.UNDEFINED else language
        return self._session._library._get_extended_error_info(language)

    def _get_warning_description(self, warning_lists: list[warnings.WarningMessage]) -> None:
        """Get warning description for SLSC warnings.
        
        Args:
            warning_lists: List of warnings captured during the operation.
        """
        self._session._get_warning_description(warning_lists)

    @classmethod
    def open_device_command(cls, session: Session, device_name: str, command_name: str) -> Self:
        """Open a reference to a device command.
        
        This allows the application to programmatically get information about
        the command at run time.
        
        Args:
            session: Previously initialized Session instance.
            device_name: Device where the command is located, or a resource
                alias such as "$DefaultDevices".
            command_name: Name of command to open.
        
        Returns:
            New instance of CommandReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")            
                session_handle = session._session_handle
                interpreter = session._interpreter
                command_handle = interpreter.open_device_command(session_handle, device_name, command_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, command_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def open_physical_channel_command(cls, session: Session, physical_channel_names: str, command_name: str) -> Self:
        """Open a reference to a physical channel command.
        
        This allows the application to programmatically get information about
        the command at run time.
        
        Args:
            session: Previously initialized Session instance.
            physical_channel_names: Physical channel where the command is
                located, or a resource alias such as "$DefaultPhysChans".
            command_name: Name of command to open.
        
        Returns:
            New instance of CommandReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")            
                session_handle = session._session_handle
                interpreter = session._interpreter
                command_handle = interpreter.open_physical_channel_command(session_handle, physical_channel_names, command_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, command_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def open_generic_command(cls, session: Session, resource: str, command_name: str) -> Self:
        """Open a reference to a command.
        
        This allows the application to programmatically get information about
        the command at run time.
        
        Args:
            session: Previously initialized Session instance.
            resource: Resource where the command is located, or a resource alias
                such as "$DefaultDevices".
            command_name: Name of command to open.
        
        Returns:
            New instance of CommandReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")            
                session_handle = session._session_handle
                interpreter = session._interpreter
                command_handle = interpreter.open_generic_command(session_handle, resource, command_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, command_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def close_command(self) -> None:
        """Close an open reference to a command."""
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")            
                self._interpreter.close_command(self._command_handle)
            if warning_list:
                self._get_warning_description(warning_list)
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_command_property_string(self, property_name: str) -> str:
        """Get the value of the specified command reflection property.
        
        Args:
            property_name: Name of command reflection property to get.
        
        Returns:
            Value of property.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")            
                property_value = self._interpreter.get_command_property_string(self._command_handle, property_name)
            if warning_list:
                self._get_warning_description(warning_list)
            return property_value
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

