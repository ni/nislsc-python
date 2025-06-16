<%!
import copy
import re
import sys
from utilities.interpreter_helpers import std_func_name, c_func_name
from utilities.function_helpers import param_placeholder, size_call, req_size, add_decl, func_call, convert_res, return_param, var_spec
%>\
import ctypes
from nislscpyapi import lib
% for function in functions:
% if 'capi' in function["targets"]:
def ${std_func_name(function)}(${", ".join([param for param in param_placeholder(function)])}):
% for line in var_spec(function):
    ${line}
% endfor
% if req_size(function):
    status = lib.niSLSC_${c_func_name(function)}(${", ".join(size_call(function))})
% for add_param in add_decl(function):
    ${add_param}
% endfor
    status = lib.niSLSC_${c_func_name(function)}(${", ".join(func_call(function))})
% else:
    status = lib.niSLSC_${c_func_name(function)}(${", ".join(func_call(function))})
% endif
% for result in convert_res(function):
    ${result}
% endfor
% if return_param(function):
    return status, ${", ".join(return_param(function))}
% else:
    return status
% endif
% endif
% endfor