<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_calling_class
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
%>\
from nislsc._library_interpreter import LibraryInterpreter

class Command():
    def __init__(self, command_handle: int, interpreter: LibraryInterpreter) -> None:
        self._command_handle = command_handle
        self._interpreter = interpreter

    def __enter__(self) -> Command:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.close_command(self._command_handle)

    def __del__(self) -> None:
        if self._command_handle is not None:
            self._interpreter.close_command(self._command_handle)

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "CommandReference" and function["name"] != "CloseCommand":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "CommandReference")])})${get_function_return_type(function)}:
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "CommandReference", False)])})

% endif
% endfor
% endif
% endfor