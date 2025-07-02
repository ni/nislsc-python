<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_calling_class
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
%>\
from nislsc._library_interpreter import LibraryInterpreter

class Property():
    def __init__(self, property_handle: int, interpreter: LibraryInterpreter) -> None:
        self._property_handle = property_handle
        self._interpreter = interpreter

    def __enter__(self) -> Property:
        return self
  
    def __exit__(self) -> None:
        self._interpreter.close_property(self._property_handle)

    def __del__(self) -> None:
        if self._property_handle is not None:
            self._interpreter.close_property(self._property_handle)

% for function in functions:
% if 'capi' in function['targets']:
% for parameter in function["params"]:
% if is_capi(parameter) and is_param_input(parameter) and parameter["dataType"] == "PropertyReference" and function["name"] != "CloseProperty":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "PropertyReference")])})${get_function_return_type(function, True)}:
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "PropertyReference", False)])})

% endif
% endfor
% endif
% endfor