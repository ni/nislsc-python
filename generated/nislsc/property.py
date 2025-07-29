"""Access SLSC property references and configuration settings.

This module provides the Property class for managing SLSC property
references that allow access to device, physical channel, and driver
configuration properties through property reflection.
"""

from __future__ import annotations
import warnings
from types import TracebackType

from typing_extensions import Self

from nislsc.constants import Language
from nislsc.error import SLSCError, SLSCWarning
from nislsc.session import Session


class Property:
    """Access SLSC property references for configuration and introspection.
    
    Create property handles to read, write, and inspect device, physical
    channel, and driver properties. Use this class to programmatically
    discover property Information and perform property reflection 
    operations.
    """

    def __init__(self, session: Session, property_handle: int) -> None:
        """Create a Property instance.

        Args:
            session: Previously initialized Session instance
            property_handle: The property handle returned by the
                initialization function.
        """
        self._property_handle = property_handle
        self._session = session
        self._interpreter = session._interpreter

    def __enter__(self) -> Self:
        """Enter the runtime context related to this object.

        Returns:
            The property object itself.
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

    def close(self) -> None:
        """Close the Property instance."""
        if self._property_handle != 0:
            self._interpreter.close_property(self._property_handle)
            self._property_handle = 0

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
    def open_device_property(cls, session: Session, device_name: str, property_name: str) -> Self:
        """Open a reference to a device property.
        
        This allows the application to programmatically get information about
        the property at run time.
        
        Args:
            session: Previously initialized Session instance.
            device_name: Device where the property is located, or a resource
                alias such as "$DefaultDevices".
            property_name: Name of property to open.
        
        Returns:
            New instance of PropertyReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                session_handle = session._session_handle
                interpreter = session._interpreter
                property_handle = interpreter.open_device_property(session_handle, device_name, property_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, property_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def open_physical_channel_property(cls, session: Session, physical_channel_names: str, property_name: str) -> Self:
        """Open a reference to a physical channel property.
        
        This allows the application to programmatically get information about
        the property at run time.
        
        Args:
            session: Previously initialized Session instance.
            physical_channel_names: Physical channel where the property is
                located, or a resource alias such as "$DefaultPhysChans".
            property_name: Name of property to open.
        
        Returns:
            New instance of PropertyReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                session_handle = session._session_handle
                interpreter = session._interpreter
                property_handle = interpreter.open_physical_channel_property(session_handle, physical_channel_names, property_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, property_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def open_driver_defined_property(cls, session: Session, property_name: str) -> Self:
        """Open a reference to a driver-defined property.
        
        This allows the application to programmatically get information about
        the property at run time.
        
        Args:
            session: Previously initialized Session instance.
            property_name: Name of property to open.
        
        Returns:
            New instance of PropertyReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                session_handle = session._session_handle
                interpreter = session._interpreter
                property_handle = interpreter.open_driver_defined_property(session_handle, property_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, property_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def open_generic_property(cls, session: Session, resource: str, property_name: str) -> Self:
        """Open a reference to a property.
        
        This allows the application to programmatically get information about
        the property at run time.
        
        Args:
            session: Previously initialized Session instance.
            resource: Resource where the property is located, or a resource
                alias such as "$DefaultDevices".
            property_name: Name of property to open.
        
        Returns:
            New instance of PropertyReference object.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                session_handle = session._session_handle
                interpreter = session._interpreter
                property_handle = interpreter.open_generic_property(session_handle, resource, property_name)
            if warning_list:
                session._get_warning_description(warning_list)
            return cls(session, property_handle)
        except SLSCError as e:
            extended_info = session._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_property_property_bool(self, property_name: str) -> bool:
        """Get the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get.
        
        Returns:
            Value of property.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                property_value = self._interpreter.get_property_property_bool(self._property_handle, property_name)
            if warning_list:
                self._get_warning_description(warning_list)
            return property_value
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_property_property_int32(self, property_name: str) -> int:
        """Get the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get.
        
        Returns:
            Value of property.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                property_value = self._interpreter.get_property_property_int32(self._property_handle, property_name)
            if warning_list:
                self._get_warning_description(warning_list)
            return property_value
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_property_property_int32_array(self, property_name: str) -> list[int]:
        """Get the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get.
        
        Returns:
            Value of property.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                property_value = self._interpreter.get_property_property_int32_array(self._property_handle, property_name)
            if warning_list:
                self._get_warning_description(warning_list)
            return property_value
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_property_property_string(self, property_name: str) -> str:
        """Get the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get.
        
        Returns:
            Value of property.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                property_value = self._interpreter.get_property_property_string(self._property_handle, property_name)
            if warning_list:
                self._get_warning_description(warning_list)
            return property_value
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_property_property_string_array(self, property_name: str) -> list[str]:
        """Get the value of the specified property reflection property.
        
        Args:
            property_name: Name of property reflection property to get.
        
        Returns:
            Value of property.
        """
        try:
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                property_value = self._interpreter.get_property_property_string_array(self._property_handle, property_name)
            if warning_list:
                self._get_warning_description(warning_list)
            return property_value
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

