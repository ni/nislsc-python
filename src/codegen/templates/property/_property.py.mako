<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from typing_extensions import Self

from nislsc._base_interpreter import BaseInterpreter
from types import TracebackType

class Property():
    """
    Represent Property class for NI SLSC.
    """

    def __init__(self, property_handle: int, interpreter: BaseInterpreter) -> None:
        """Initialize a Property instance.

        Args:
            property_handle: The property handle returned by the
                initialization function.
            interpreter: The interpreter instance used for
                communication.
        """
        self._property_handle = property_handle
        self._interpreter = interpreter

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

    def __del__(self) -> None:
        """
        Remind the user that the Property instance is not closed.
        """
        if self._session_handle is not None:
            warnings.warn(
                'Property was not closed before it was destructed. Resources on the'
                'Property may still be reserved.',
                SLSCResourceWarning
            )

    def close(self) -> None:
        """
        Close the Property instance.
        """
        if self._property_handle is not None:
            self._interpreter.close_property(self._property_handle)
            self._property_handle = None

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "PropertyReference" and function["name"] != "CloseProperty":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "PropertyReference")])})${get_function_return_type(function, True)}:
% for docstrings in generate_docstrings(function, "PropertyReference"):
        ${docstrings}
% endfor
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "PropertyReference", False)])})

% endif
% endfor
% endif
% endfor