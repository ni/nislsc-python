<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from nislsc._base_interpreter import BaseInterpreter
from types import TracebackType

class Property():
    """Represents a property object for NI SLSC.

    This class manages the property handle and interpreter, and provides
    context management and resource cleanup for SLSC properties.
    """

    def __init__(self, property_handle: int, interpreter: BaseInterpreter) -> None:
        """Initializes a Property instance.

        Args:
            property_handle (int): The property handle returned by the
                initialization function.
            interpreter (BaseInterpreter): The interpreter instance used for
                communication.
        """
        self._property_handle = property_handle
        self._interpreter = interpreter

    def __enter__(self) -> "Property":
        """Enter the runtime context related to this object.

        Returns:
            Property: The property object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the property handle.

        Args:
            type (type[BaseException] | None): The exception type, if an
                exception was raised, otherwise None.
            value (BaseException | None): The exception value, if an exception
                was raised, otherwise None.
            traceback (TracebackType | None): The traceback, if an exception was
                raised, otherwise None.
        """
        self._interpreter.close_property(self._property_handle)
        self._property_handle = 0

    def __del__(self) -> None:
        """Destructor to ensure the property is closed when the object is
        deleted.
        """
        if self._property_handle != 0:
            self._interpreter.close_property(self._property_handle)

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