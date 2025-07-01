<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_calling_class
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
%>\
from nislsc._library_interpreter import LibraryInterpreter
from nislsc.constants import Language

class Library():
    def __init__(self, version) -> None:
        self._interpreter = LibraryInterpreter()
        self._library_handle = self._interpreter.initialize_library(self._interpreter.get_library_version())
        self._language = Language.CURRENT_THREAD_LOCALE

    def __enter__(self) -> Library:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.finalize_library(self._library_handle)

    def __del__(self) -> None:
        if self._library_handle is not None:
            self._interpreter.finalize_library(self._library_handle)

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "Library" and function["name"] != "FinalizeLibrary":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library")])})${get_function_return_type(function)}:
% if is_calling_class(function, "Session"):
        return Session(self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", False)])}), self._interpreter)

% else:
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", False)])})

% endif
% endif
% endfor
% endif
% endfor