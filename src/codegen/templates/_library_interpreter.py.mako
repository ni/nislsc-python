<%!
from utilities.interpreter_helpers import get_python_function_name, get_capi_function_name, get_standardized_param_name
from utilities.function_helpers import get_function_parameter_list, generate_function_call_for_size, is_size_unknown, generate_additional_variable_declaration, generate_function_call_for_result, generate_result_parser, generate_return_parameter, generate_variable_declaration, get_ctypes_argtypes, get_function_return_type, generate_function_call_validation
%>\
import ctypes

from _base_interpreter import BaseInterpreter
from error import SLSCError, SLSCWarning
import warnings

lib = ctypes.CDLL('nislsc.dll')

% for function in functions:
% if 'capi' in function['targets']:
lib.niSLSC_${get_capi_function_name(function)}.restype = ctypes.c_int32
lib.niSLSC_${get_capi_function_name(function)}.argtypes = [${", ".join([param for param in get_ctypes_argtypes(function)])}]

% endif
% endfor
class LibraryInterpreter(BaseInterpreter):

% for function in functions:
% if 'capi' in function["targets"]:
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function)])})${get_function_return_type(function)}:
% for line in generate_variable_declaration(function):
        ${line}
% endfor
% if is_size_unknown(function):
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_size(function))})
        if ${generate_function_call_validation(function)}:
            self.check_for_error(None, status)
% for add_param in generate_additional_variable_declaration(function):
        ${add_param}
% endfor
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_result(function))})
        self.check_for_error(None, status)
% else:
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_result(function))})
        self.check_for_error(None, status)
% endif
% for result in generate_result_parser(function):
        ${result}
% endfor
        return ${", ".join(generate_return_parameter(function))}

% endif
% endfor
    def check_for_error(self, library_handle: int, error_code: int) -> None:
        if error_code == 0:
            return
        if library_handle is None:
            if error_code < 0:
                raise SLSCError("", error_code)
            elif error_code > 0:
                warnings.warn(SLSCWarning("", error_code))
            return
        library_handle = ctypes.c_void_p(library_handle)
        extended_error_info = self.get_extended_error_info(library_handle, language=0)
        if error_code < 0:
            raise SLSCError(extended_error_info, error_code)
        elif error_code > 0:
            warnings.warn(SLSCWarning(extended_error_info, error_code))
