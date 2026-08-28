<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_defining_language, is_class_func, generate_return_in_class, generate_function_call_in_class
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
"""Initialize and manage the SLSC library interface.

This module provides the Library class for managing the SLSC library 
interface that handles driver initialization, error management, and
language configuration for SLSC hardware operations. 
"""

from __future__ import annotations
from types import TracebackType

from typing_extensions import Self

from nislsc.constants import Language
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
        self._interpreter._library_handle = self.initialize_library(get_library_version())
        self._interpreter._language = language

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
        return self._interpreter._language

    @language.setter
    def language(self, language: Language) -> None:
        """Set the language for error messages and other outputs.

        Args:
            language: The language to set.
        """
        self._interpreter._language = language

    def close(self) -> None:
        """Close the Library instance."""
        if self._interpreter._library_handle != 0:
            self._interpreter.finalize_library(self._interpreter._library_handle)
            self._interpreter._library_handle = 0

% for function in functions:
% if 'capi' in function['targets']:
% if is_class_func(function, "Library") and function["name"] != "FinalizeLibrary" and function["name"] != "GetExtendedErrorInfo":
    def ${get_python_function_name(function, True)}(${", ".join([param for param in get_function_parameter_list(function, "Library", is_language=True, include_defaults=True)])})${get_function_return_type(function)}:
% for docstrings in generate_docstrings(function, "Library"):
        ${docstrings}
% endfor
% if is_defining_language(function):
        language = self._interpreter._language if language == Language.UNDEFINED else language
% endif
% for function_call in generate_function_call_in_class(function, 'Library'):
        ${function_call}
% endfor
% for result in generate_return_in_class(function):
        ${result}
% endfor

% endif
% endif
% endfor