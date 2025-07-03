<%!
from utilities.docstrings_helpers import generate_docstrings
from utilities.function_helpers import get_function_parameter_list, get_function_return_type
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input

def remove_all_class_functions(function: dict) -> bool:
    """Removes all functions that are not intended for the SLSC class."""
    for param in function['params']:
        if param['dataType'] in ("Library", "Session", "PropertyReference", "CommandReference"):
            return False
    return True
%>\
from nislsc._library_interpreter import LibraryInterpreter
from nislsc.library._library import Library
from nislsc.constants import Language

class NISLSC():
    """Represents the NI SLSC interface.

    This class provides methods to initialize the SLSC library and access its functions.
    It manages the library interpreter and provides a context manager for resource cleanup.
    """
    def __init__(self) -> None:
        """Initializes the SLSC interface."""
        self._interpreter = LibraryInterpreter()

    def initialize_library(self, version: int = 0, language: Language = Language.CURRENT_THREAD_LOCALE) -> Library:
        """Initializes the SLSC library.

        Args:
            version (int): The version of the library to initialize.
            language (Language): The language to use for error messages and outputs.

        Returns:
            int: The library handle.
        """
        return Library(self._interpreter.initialize_library(version or self._interpreter.get_library_version()), self._interpreter, language)

% for function in functions:
% if 'capi' in function['targets']:
% if remove_all_class_functions(function):
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter):
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function)])})${get_function_return_type(function)}:
% for docstrings in generate_docstrings(function):
        ${docstrings}
% endfor
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "", False)])})

% endif
% endfor
% endif
% endif
% endfor