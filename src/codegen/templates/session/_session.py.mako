<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_calling_class
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
%>\
from nislsc._library_interpreter import LibraryInterpreter

class Session():
    def __init__(self, session_handle: int, interpreter: LibraryInterpreter) -> None:
        self._session_handle = session_handle
        self._interpreter = interpreter

    def __enter__(self) -> Session:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.close_session(self._session_handle)

    def __del__(self) -> None:
        if self._session_handle is not None:
            self._interpreter.close_session(self._session_handle)

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "Session" and function["name"] != "CloseSession":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session")])})${get_function_return_type(function)}:
% if is_calling_class(function, "PropertyReference"):
        return Property(self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])}), self._interpreter)

% elif is_calling_class(function, "CommandReference"):
        return Command(self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])}), self._interpreter)

% else:
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Session", False)])})

% endif
% endif
% endfor
% endif
% endfor