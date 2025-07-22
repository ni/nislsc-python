<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_class_func, generate_return, is_classmethod, get_classmethod_parameter_list
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from typing_extensions import Self

from nislsc.session._session import Session
from types import TracebackType

class Property():
    """
    Represent Property class for NI SLSC.
    """

    def __init__(self, session: Session, property_handle: int) -> None:
        """Initialize a Property instance.

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
% for result in generate_return(function, 'PropertyReference'):
        ${result}
% endfor

% endif
% endif
% endfor