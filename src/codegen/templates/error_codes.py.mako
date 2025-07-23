<%!
from utilities.interpreter_helpers import convert_to_snake_case

def remove_k_prefix(s: str) -> str:
    if s.upper().startswith("K_ERROR"):
        return s[8:]
    elif s.upper().startswith("K_WARNING"):
        return s[10:]
    return s
%>\
"""SLSC Error Codes and Warning Definitions Module.

This module provides enumeration classes that define error codes and
warning codes returned by SLSC API operations.
"""

from enum import Enum

__all__ = ['SLSCErrors', 'SLSCWarnings']

class SLSCErrors(Enum):
    UNKNOWN = -1
%for error in errors:
% if error['code'] < 0:
    ${remove_k_prefix(convert_to_snake_case(error['symbol']).upper())} = ${error['code']}
% endif
%endfor

class SLSCWarnings(Enum):
    UNKNOWN = -1
%for error in errors:
% if error['code'] > 0:
    ${remove_k_prefix(convert_to_snake_case(error['symbol']).upper())} = ${error['code']}
% endif
%endfor