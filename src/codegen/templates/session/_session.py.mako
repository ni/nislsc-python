<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_class_func, generate_return, is_classmethod, get_classmethod_parameter_list
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
"""SLSC Session Management Module.

This module provides the Session class for managing SLSC hardware
sessions that handle device connections, property access, command 
execution for one or more devices, physical channels, or NVMEM areas.
"""

import warnings
from types import TracebackType

from typing_extensions import Self

from nislsc.error import SLSCResourceWarning
from nislsc.library._library import Library


class Session:
    """Represent Session class for NI SLSC."""

    def __init__(self, library: Library, session_handle: int) -> None:
        """Create a Session instance.

        Args:
            library: Previously initialized Library instance
            session_handle: The session handle returned by the
                initialization function.
        """
        self._session_handle = session_handle
        self._library = library
        self._interpreter = library._interpreter

    def __enter__(self) -> Self:
        """Enter the runtime context related to this object.

        Returns:
            Self: The session object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the Session instance.

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
        """Close the Session instance."""
        if self._session_handle is not None:
            self._interpreter.close_session(self._session_handle)
            self._session_handle = None

% for function in functions:
% if 'capi' in function['targets']:
% if is_class_func(function, "Session") and function["name"] != "CloseSession":
% if is_classmethod(function, "Session"):
    @classmethod
    def ${get_python_function_name(function)}(${", ".join([param for param in get_classmethod_parameter_list(function)])})${get_function_return_type(function, True)}:
% else:
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session")])})${get_function_return_type(function, True)}:
% endif:
% if is_classmethod(function, "Session"):
% for docstrings in generate_docstrings(function, "Session", True):
        ${docstrings}
% endfor
% else:
% for docstrings in generate_docstrings(function, "Session"):
        ${docstrings}
% endfor
% endif
% for result in generate_return(function, 'Session'):
        ${result}
% endfor

% endif
% endif
% endfor