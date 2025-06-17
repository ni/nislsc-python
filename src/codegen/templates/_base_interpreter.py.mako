<%!
import copy
import re
import sys
from utilities.interpreter_helpers import std_func_name, c_func_name
from utilities.function_helpers import param_placeholder, size_call, req_size, add_decl, func_call, convert_res, return_param, var_spec, arg_placeholder
%>\
import abc
class BaseInterpreter(abc.ABC):
% for function in functions:
% if 'capi' in function["targets"]:
    @abc.abstractmethod
    def ${std_func_name(function)}(${", ".join([param for param in param_placeholder(function)])}):
        pass
% endif
% endfor

