<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from nislsc._base_interpreter import BaseInterpreter
from nislsc.command._command import Command
from nislsc.property._property import Property
from types import TracebackType

class Session():
    """Represents a session for interacting with the NI SLSC hardware.

    This class manages the session handle and interpreter, and provides
    context management and resource cleanup for SLSC sessions.
    """
    def __init__(self, session_handle: int, interpreter: BaseInterpreter) -> None:
        """Initializes a Session instance.

        Args:
            session_handle (int): The session handle returned by the
                initialization function.
            interpreter (BaseInterpreter): The interpreter instance used for
                communication.
        """
        self._session_handle = session_handle
        self._interpreter = interpreter

    def __enter__(self) -> "Session":
        """Enter the runtime context related to this object.

        Returns:
            Session: The session object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the session.

        Args:
            type (type[BaseException] | None): The exception type, if an
                exception was raised, otherwise None.
            value (BaseException | None): The exception value, if an exception
                was raised, otherwise None.
            traceback (TracebackType | None): The traceback, if an exception was
                raised, otherwise None.
        """
        self._interpreter.close_session(self._session_handle)
        self._session_handle = 0

    def __del__(self) -> None:
        """Destructor to ensure the session is closed when the object is 
        deleted.
        """
        if self._session_handle != 0:
            self._interpreter.close_session(self._session_handle)

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "Session" and function["name"] != "CloseSession":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session")])})${get_function_return_type(function, True)}:
% for docstrings in generate_docstrings(function, "Session"):
        ${docstrings}
% endfor
% if is_creating_handle(function, "PropertyReference"):
        return Property(self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])}), self._interpreter)
% elif is_creating_handle(function, "CommandReference"):
        return Command(self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])}), self._interpreter)
% else:
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])})
% endif

% endif
% endfor
% endif
% endfor