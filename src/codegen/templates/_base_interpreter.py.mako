<%!
import copy
import re
import sys
from utilities.interpreter_helpers import std_func_name
from utilities.function_helpers import param_placeholder, param_types
%>\
import abc

from typing import Tuple, List

class BaseInterpreter(abc.ABC):

% for function in functions:
% if 'capi' in function["targets"]:
    @abc.abstractmethod
    def ${std_func_name(function)}(${", ".join([param for param in param_placeholder(function)])})${param_types(function)}:
        pass

% endif
% endfor

