<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_class_func
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from typing_extensions import Self

from nislsc._base_interpreter import BaseInterpreter
from nislsc.command._command import Command
from nislsc.property._property import Property
from nislsc.utils import _select_interpreter
from types import TracebackType

class Session():
    """
    Represent Session class for NI SLSC.
    """
    def __init__(self, library: Library, session_handle: int, interpreter: BaseInterpreter) -> None:
        """Initialize a Session instance.

        Args:
            library: The library instance used for session
                management.
            session_handle: The session handle returned by the
                initialization function.
            interpreter: The interpreter instance used for
                communication.
        """
        self._session_handle = session_handle
        self._interpreter = _select_interpreter()

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
        self._close()

    def __del__(self) -> None:
        """
        Remind the user that the Session instance is not closed.
        """
        if self._session_handle is not None:
            warnings.warn(
                'Session was not closed before it was destructed. Resources on the'
                'Session may still be reserved.',
                SLSCResourceWarning
            )

    def close(self) -> None:
        """
        Close the Session instance.
        """
        if self._session_handle is not None:
            self._interpreter.close_session(self._session_handle)
            self._session_handle = None

% for function in functions:
% if 'capi' in function['targets']:
% if is_class_func(function, "Session") and function["name"] != "CloseSession":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session")])})${get_function_return_type(function, True)}:
% for docstrings in generate_docstrings(function, "Session"):
        ${docstrings}
% endfor
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])})

% endif
% endif
% endfor