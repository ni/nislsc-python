<%!
import copy
import re
import sys
from utilities.interpreter_helpers import std_func_name, c_func_name
from utilities.function_helpers import param_placeholder, size_call, req_size, add_decl, func_call, convert_res, return_param, var_spec, arg_placeholder, param_types
%>\

import ctypes

from typing import Tuple, List
from nislsc._base_interpreter import BaseInterpreter
from nislsc.error import SLSCError, SLSCWarning, status_message

lib = ctypes.CDLL('nislsc.dll')

% for function in functions:
% if 'capi' in function['targets']:
lib.niSLSC_${c_func_name(function)}.restype = ctypes.c_int32
lib.niSLSC_${c_func_name(function)}.argtypes = [${", ".join([param for param in arg_placeholder(function)])}]

% endif
% endfor
class LibraryInterpreter(BaseInterpreter):
% for function in functions:
% if 'capi' in function["targets"]:
    def ${std_func_name(function)}(${", ".join([param for param in param_placeholder(function)])})${param_types(function)}:
% for line in var_spec(function):
        ${line}
% endfor
% if req_size(function):
        status = lib.niSLSC_${c_func_name(function)}(${", ".join(size_call(function))})
% for add_param in add_decl(function):
        ${add_param}
% endfor
        status = lib.niSLSC_${c_func_name(function)}(${", ".join(func_call(function))})
        if status < 0:
                raise SLSCError(status, status)
        elif status > 0:
                warnings.warn(SLSCWarning(status, status))
% else:
        status = lib.niSLSC_${c_func_name(function)}(${", ".join(func_call(function))})
        if status < 0:
                raise SLSCError(status, status)
        elif status > 0:
                warnings.warn(SLSCWarning(status, status))
% endif
% for result in convert_res(function):
        ${result}
% endfor
        return ${", ".join(return_param(function))}

% endif
% endfor

 def get_extended_error_info(self):
        error_buffer = ctypes.create_string_buffer(2048)

        cfunc = lib_importer.windll.DAQmxGetExtendedErrorInfo
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [ctypes.c_char_p, ctypes.c_uint]

        query_error_code = cfunc(error_buffer, 2048)
        if query_error_code < 0:
            _logger.error('Failed to get extended error info. DAQmxGetExtendedErrorInfo returned error code %d.', query_error_code)
            return 'Failed to retrieve error description.'
        return error_buffer.value.decode(lib_importer.encoding)

def check_for_error(self, error_code):
        if not error_code:
                return

        if error_code < 0:
                extended_error_info = self.get_extended_error_info()
                raise SLSCError(extended_error_info, error_code)

        elif error_code > 0:
                error_string = self.get_error_string(error_code)

                warnings.warn(DaqWarning(error_string, error_code))