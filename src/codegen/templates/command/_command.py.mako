<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from typing_extensions import Self

import warnings
from types import TracebackType

from nislsc._base_interpreter import BaseInterpreter
from nislsc.error import SLSCResourceWarning

class Command():
    """
    Represent Command class for NI SLSC.
    """
    def __init__(self, command_handle: int, interpreter: BaseInterpreter) -> None:
        """Initialize a Command instance.

        Args:
            command_handle: The command handle returned by the
                initialization function.
            interpreter: The interpreter instance used for
                communication.
        """
        self._command_handle = command_handle
        self._interpreter = interpreter

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

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "CommandReference" and function["name"] != "CloseCommand":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "CommandReference")])})${get_function_return_type(function)}:
% for docstrings in generate_docstrings(function, "CommandReference"):
        ${docstrings}
% endfor
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "CommandReference", False)])})

% endif
% endfor
% endif
% endfor