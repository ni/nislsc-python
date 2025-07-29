"""Initialize and manage the SLSC library interface.

This module provides the Library class for managing the SLSC library 
interface that handles driver initialization, error management, and
language configuration for SLSC hardware operations. 
"""

from __future__ import annotations
import warnings
from types import TracebackType

from typing_extensions import Self

from nislsc.constants import Language
from nislsc.error import SLSCError, SLSCWarning
from nislsc.utils import _select_interpreter, get_library_version


class Library:
    """Initialize SLSC driver software interface.
    
    Create a library handle to access SLSC driver functionality and manage
    driver resources. This class provides the foundation for creating
    sessions that connect to actual hardware devices.
    """

    def __init__(self, language: Language = Language.CURRENT_THREAD_LOCALE) -> None:
        """Create a Library instance.

        Args:
            language: The language to use for error messages and outputs.
        """
        self._interpreter = _select_interpreter()
        self._library_handle = self.initialize_library(get_library_version())
        self._language = language

    def __enter__(self) -> Self:
        """Enter the runtime context related to this object.

        Returns:
           The library object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and finalize the Library instance.

        Args:
            type: The exception type, if an exception was raised, otherwise 
                None.
            value: The exception value, if an exception was raised, otherwise
                None.
            traceback: The traceback, if an exception was raised, otherwise 
                None.
        """
        self.close()

    @property
    def language(self) -> Language:
        """Get the current language setting.

        Returns:
            An enum representing the current language.
        """
        return self._language

    @language.setter
    def language(self, language: Language) -> None:
        """Set the language for error messages and other outputs.

        Args:
            language: The language to set.
        """
        self._language = language

    def close(self) -> None:
        """Close the Library instance."""
        if self._library_handle != 0:
            self._interpreter.finalize_library(self._library_handle)
            self._library_handle = 0

    def _get_warning_description(self, warning_lists: list[warnings.WarningMessage]) -> None:
        """Get warning description for SLSC warnings.
        
        Args:
            warning_lists: List of warnings captured during the operation.
        """
        for warning_list in warning_lists:
            if isinstance(warning_list.message, SLSCWarning):
                error_code = warning_list.message.error_code
                message = self.get_error_description(
                    warning_list.message.error_code
                )
                if message:
                    warnings.warn(SLSCWarning(message, error_code))
                else:
                    warnings.warn(warning_list.message)

    def initialize_library(self, version: int) -> int:
        """Return a library handle to identify the SLSC library.
        
        You must call this function at least once for the application.
        
        The 'version' parameter must be set to the NISLSC_LIBRARY_VERSION
        constant. If you are building a DLL, do not call InitializeLibrary from
        DllMain or a C++ static initializer/destructor.
        
        Args:
            version: Version of the SLSC library used to compile this
                application. Pass NISLSC_LIBRARY_VERSION for this parameter.
        
        Returns:
            New instance of Library object.
        """
        try:
            library_handle = self._interpreter.initialize_library(version)
            return library_handle
        except SLSCError as e:
            raise SLSCError(f"Failed to initialize library. Error code: {e.error_code}", e.error_code)

    def _get_extended_error_info(self, language: Language = Language.UNDEFINED) -> str:
        """Return extended error information for the last error that occurred on
        the specified library handle.
        
        Args:
            language: Language to return error information in.
        
        Returns:
            Extended error info text.
        """
        try:
            language = self._language if language == Language.UNDEFINED else language
            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                extended_error_info = self._interpreter.get_extended_error_info(self._library_handle, language)
            if warning_list:
                self._get_warning_description(warning_list)
            return extended_error_info
        except SLSCError as e:
            raise SLSCError(f"Failed to get extended error information. Error code: {e.error_code}", e.error_code)

    def get_error_description(self, status_code: int, language: Language = Language.UNDEFINED) -> str:
        """Return the error description for the specified status code.
        
        Args:
            status_code: Status code to look up.
            language: Language to return error information in.
        
        Returns:
            Error description text.
        """
        try:
            language = self._language if language == Language.UNDEFINED else language
            error_description = self._interpreter.get_error_description(self._library_handle, status_code, language)
            return error_description
        except SLSCError as e:
            extended_info = self._get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

