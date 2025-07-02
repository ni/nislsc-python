<%!
from utilities.interpreter_helpers import get_python_function_name
from utilities.function_helpers import get_function_parameter_list, get_function_return_type
%>\
import abc
from nislsc.constants import Language

class BaseInterpreter(abc.ABC):

% for function in functions:
% if 'capi' in function["targets"]:
    @abc.abstractmethod
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function)])})${get_function_return_type(function)}:
        pass

% endif
% endfor

