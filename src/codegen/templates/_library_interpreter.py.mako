<%!
import copy
import re
import sys
from utilities.interpreter_helpers import std_func_name, c_func_name, std_var_name
from utilities.function_helpers import param_placeholder, size_call, req_size, add_decl, func_call, convert_res, return_param, var_spec, arg_placeholder, param_types, gen_val
%>\
import ctypes

from typing import Tuple, List
from _base_interpreter import BaseInterpreter
from error import SLSCError, SLSCWarning
import warnings

lib = ctypes.CDLL('nislsc.dll')

% for function in functions:
% if 'capi' in function['targets']:
lib.niSLSC_${c_func_name(function)}.restype = ctypes.c_int32
lib.niSLSC_${c_func_name(function)}.argtypes = [${", ".join([param for param in arg_placeholder(function)])}]

% endif
% endfor
class LibraryInterpreter(BaseInterpreter):

    def __init__(self) -> None:
        self._language = 0

    @property
    def language(self) -> int:
        return self._language

    @language.setter
    def language(self, value: int) -> None:
        self._language = value

% for function in functions:
% if 'capi' in function["targets"]:
    def ${std_func_name(function)}(${", ".join([param for param in param_placeholder(function)])})${param_types(function)}:
% for line in var_spec(function):
        ${line}
% endfor
% if req_size(function):
        status = lib.niSLSC_${c_func_name(function)}(${", ".join(size_call(function))})
        if ${gen_val(function)}:
            self.check_for_error(status, library_handle.value)
% for add_param in add_decl(function):
        ${add_param}
% endfor
        status = lib.niSLSC_${c_func_name(function)}(${", ".join(func_call(function))})
        self.check_for_error(status, library_handle.value)
% else:
        status = lib.niSLSC_${c_func_name(function)}(${", ".join(func_call(function))})
        self.check_for_error(status, library_handle.value)
% endif
% for result in convert_res(function):
        ${result}
% endfor
        return ${", ".join(return_param(function))}

% endif
% endfor
    def check_for_error(self, error_code: int, library_handle: int = None) -> None:
        if library_handle is None:
            extended_error_info = "Library Handle is not provided"
            warnings.warn(SLSCWarning(extended_error_info, -1))
            return
        library_handle = ctypes.c_void_p(library_handle)
        if error_code == 0:
            return
        if error_code < 0:
            extended_error_info = self.get_extended_error_info(library_handle, self._language)
            raise SLSCError(extended_error_info, error_code)
        elif error_code > 0:
            extended_error_info = self.get_extended_error_info(library_handle, self._language)
            warnings.warn(SLSCWarning(extended_error_info, error_code))
