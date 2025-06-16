<%!
import copy
import re
import sys
from utilities.interpreter_helpers import c_func_name
from utilities.declaration_helpers import arg_placeholder
%>\
import ctypes
lib = ctypes.CDLL('nislsc.dll')
% for function in functions:
% if 'capi' in function['targets']:
lib.niSLSC_${c_func_name(function)}.restype = ctypes.c_int32
lib.niSLSC_${c_func_name(function)}.argtypes = [${", ".join([param for param in arg_placeholder(function)])}]
% endif
% endfor