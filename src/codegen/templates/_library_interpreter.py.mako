<%!
from utilities.interpreter_helpers import get_python_function_name, get_capi_function_name, get_standardized_param_name
from utilities.function_helpers import get_function_parameter_list, generate_function_call_for_size, is_size_unknown, generate_additional_variable_declaration, generate_function_call_for_result, generate_result_parser, generate_return_parameter, generate_variable_declaration, get_ctypes_argtypes, get_function_return_type, generate_conditional_for_validation
%>\
"""Provide ctypes-based SLSC library implementation.

This module provides the LibraryInterpreter class, a concrete
implementation of the BaseInterpreter abstract interface that uses
ctypes to interface directly with the native SLSC C library.
"""

import ctypes
import warnings

from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language, ReservationAccess, TableScaleCoercion
from nislsc.error import SLSCError, SLSCWarning


lib = ctypes.CDLL("nislsc.dll")

% for function in functions:
% if "capi" in function["targets"]:
lib.niSLSC_${get_capi_function_name(function)}.restype = ctypes.c_int32
lib.niSLSC_${get_capi_function_name(function)}.argtypes = [${", ".join([param for param in get_ctypes_argtypes(function)])}]

% endif
% endfor
class LibraryInterpreter(BaseInterpreter):

    def __init__(self) -> None:
        super().__init__()

    def _check_for_error(self, error_code: int) -> None:
        if error_code != 0:
            if error_code < 0:
                error_description = self.get_extended_error_info(self._library_handle, self._language)
                raise SLSCError(error_description, error_code)
            elif error_code > 0:
                warning_description = self.get_error_description(self._library_handle, error_code, self._language)
                warnings.warn(SLSCWarning(warning_description, error_code))

% for function in functions:
% if "capi" in function["targets"]:
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function)])})${get_function_return_type(function)}:
% for line in generate_variable_declaration(function):
        ${line}
% endfor
% if is_size_unknown(function):
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_size(function))})
        if ${generate_conditional_for_validation(function)}:
% if function["name"] == "GetExtendedErrorInfo":
            raise SLSCError("GetExtendedErrorInfo is not supported in this context.", -1)
% elif function["name"] == "GetErrorDescription":
            if status < 0:
                self._check_for_error(status)
% else:
            self._check_for_error(status)
% endif
% for add_param in generate_additional_variable_declaration(function):
        ${add_param}
% endfor
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_result(function))})
% if function["name"] == "GetExtendedErrorInfo":
        if status < 0:
            raise SLSCError("GetExtendedErrorInfo is not supported in this context.", -1)
% elif function["name"] == "GetErrorDescription":
        if status < 0:
            self._check_for_error(status)
% else:
        self._check_for_error(status)
% endif
% else:
        status = lib.niSLSC_${get_capi_function_name(function)}(${", ".join(generate_function_call_for_result(function))})
% if function["name"] == "GetExtendedErrorInfo":
        if status < 0:
            self._check_for_error(status)
% elif function["name"] == "GetErrorDescription":
        if status < 0:
            self._check_for_error(status)
% else:
        self._check_for_error(status)
% endif
% endif
% for result in generate_result_parser(function):
        ${result}
% endfor
        return ${", ".join(generate_return_parameter(function))}

% endif
% endfor
