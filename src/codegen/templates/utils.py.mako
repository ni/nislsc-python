<%!
from utilities.docstrings_helpers import generate_docstrings
from utilities.function_helpers import get_function_parameter_list, get_function_return_type
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input

def remove_all_class_functions(function: dict) -> bool:
    """Remove all functions that are not intended for the SLSC class."""
    for param in function['params']:
        if param['dataType'] in ("Library", "Session", "PropertyReference", "CommandReference"):
            return False
    return True
%>\
"""Provide SLSC utility functions.

This module provides utility functions for SLSC operations including
interpreter selection, library version retrieval, and name formatting
utilities for device, physical channel, and NVMEM area identifiers.
"""

from nislsc._base_interpreter import BaseInterpreter

def _select_interpreter() -> BaseInterpreter:
    """Select the appropriate interpreter based on the environment.

    We only support Library Interpreter for now.
    """
    from nislsc._library_interpreter import LibraryInterpreter

    return LibraryInterpreter()

% for function in functions:
% if 'capi' in function['targets']:
% if remove_all_class_functions(function):
def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, None, True, False, False)])})${get_function_return_type(function)}:
% for docstrings in generate_docstrings(function):
    ${docstrings}
% endfor
    _interpreter = _select_interpreter()
    return _interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "", False)])})

% endif
% endif
% endfor