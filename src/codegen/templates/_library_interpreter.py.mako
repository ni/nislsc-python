<%!
from utilities.interpreter_helpers import get_python_function_name, get_capi_function_name, get_standardized_param_name
from utilities.function_helpers import get_function_parameter_list, generate_function_call_for_size, is_size_unknown, generate_additional_variable_declaration, generate_function_call_for_result, generate_result_parser, generate_return_parameter, generate_variable_declaration, get_ctypes_argtypes, get_function_return_type, generate_conditional_for_validation, has_library_handle
%>\
import ctypes

from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language
from nislsc.error import SLSCError, SLSCWarning
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
        if ${generate_conditional_for_validation(function)}:
            self.check_for_error(${has_library_handle(function)}, status)
% for add_param in generate_additional_variable_declaration(function):
        ${add_param}
% endfor
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_result(function))})
        self.check_for_error(${has_library_handle(function)}, status)
% else:
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_result(function))})
        self.check_for_error(${has_library_handle(function)}, status)
% endif
% for result in generate_result_parser(function):
        ${result}
% endfor
        return ${", ".join(generate_return_parameter(function))}

% endif
% endfor
    def check_for_error(self, library_handle: int | None, error_code: int) -> None:
        if error_code != 0:
            extended_error_info = ""
            if library_handle is not None:
                extended_error_info = self.get_extended_error_info(library_handle, language=Language.CURRENT_THREAD_LOCALE)
            if error_code < 0:
                raise SLSCError(extended_error_info, error_code)
            elif error_code > 0:
                warnings.warn(SLSCWarning(extended_error_info, error_code))

