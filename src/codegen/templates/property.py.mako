<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_class_func, is_classmethod, get_classmethod_parameter_list, generate_return_in_class, generate_function_call_in_class
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
"""SLSC Property Management Module.

This module provides the Property class for managing SLSC property
references that allow access to device, physical channel, and driver
configuration properties through property reflection.
"""

from __future__ import annotations
from types import TracebackType

from typing_extensions import Self

from nislsc.error import SLSCError
from nislsc.session._session import Session


class Property:
    """Represent Property class for NI SLSC."""

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

    def close(self) -> None:
        """Close the Property instance."""
        if self._property_handle != 0:
            self._interpreter.close_property(self._property_handle)
            self._property_handle = 0

        def get_extended_error_info(self, language: Language = Language.UNDEFINED) -> str:
        """Return extended error information for the last error that occurred on
        the specified library handle.
        
        Args:
            language: Language to return error information in
        
        Returns:
            extended_error_info: Extended error info text
        """
        language = self._session._library.language if language == language.UNDEFINED else language
        return self._session._library.get_extended_error_info(language)

% for function in functions:
% if 'capi' in function['targets']:
% if is_class_func(function, "PropertyReference") and function["name"] != "CloseProperty":
% if is_classmethod(function, "PropertyReference"):
    @classmethod
    def ${get_python_function_name(function)}(${", ".join([param for param in get_classmethod_parameter_list(function)])})${get_function_return_type(function, True)}:
% else:
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "PropertyReference")])})${get_function_return_type(function, True)}:
% endif:
% if is_classmethod(function, "PropertyReference"):
% for docstrings in generate_docstrings(function, "PropertyReference", True):
        ${docstrings}
% endfor
% else:
% for docstrings in generate_docstrings(function, "PropertyReference"):
        ${docstrings}
% endfor
% endif
        try:
% for function_call in generate_function_call_in_class(function, 'PropertyReference'):
            ${function_call}
% endfor
% for result in generate_return_in_class(function):
            ${result}
% endfor
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

% endif
% endif
% endfor