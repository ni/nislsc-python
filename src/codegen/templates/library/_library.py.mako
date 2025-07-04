<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_defining_language
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language
from nislsc.session._session import Session
from types import TracebackType

class Library():
    """Represents the NI SLSC Library interface.

    This class manages the library handle and interpreter, and provides methods
    for session initialization, error handling, and resource management.
    """
    def __init__(self, library_handle: int, interpreter: BaseInterpreter, language: Language = Language.CURRENT_THREAD_LOCALE) -> None:
        """Initializes a Library instance.

        Args:
            library_handle (int): The library handle returned by the initialization function.
            interpreter (BaseInterpreter): The interpreter instance used for communication.
            language (Language): The language to use for error messages and outputs.
        """
        self._library_handle = library_handle
        self._interpreter = interpreter
        self._language = language

    def __enter__(self) -> "Library":
        """Enter the runtime context related to this object.

        Returns:
            Library: The library object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and finalize the library handle.

        Args:
            type (type[BaseException] | None): The exception type, if an exception was raised, otherwise None.
            value (BaseException | None): The exception value, if an exception was raised, otherwise None.
            traceback (TracebackType | None): The traceback, if an exception was raised, otherwise None.
        """
        self._interpreter.finalize_library(self._library_handle)
        self._library_handle = 0

    def __del__(self) -> None:
        """Destructor to ensure the library is finalized when the object is deleted."""
        if self._library_handle != 0:
            self._interpreter.finalize_library(self._library_handle)

    @property
    def language(self) -> Language:
        """Gets the current language setting.

        Returns:
            Language: An enum representing the current language.
        """
        return self._language

    @language.setter
    def language(self, language: Language) -> None:
        """Sets the language for error messages and other outputs.

        Args:
            language (Language): The language to set.
        """
        self._language = language

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "Library" and function["name"] != "FinalizeLibrary":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", True, True)])})${get_function_return_type(function, True)}:
% for docstrings in generate_docstrings(function, "Library"):
        ${docstrings}
% endfor
% if is_defining_language(function):
        language = self._language if language == Language.UNDEFINED else language
% endif
% if is_creating_handle(function, "Session"):
        return Session(self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", False)])}), self._interpreter)
% else:
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", False)])})
% endif

% endif
% endfor
% endif
% endfor