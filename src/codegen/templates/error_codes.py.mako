<%!
    from utilities.interpreter_helpers import convert_to_snake_case

    def remove_k_prefix(s: str) -> str:
        if s.upper().startswith("K_"):
            return s[2:]
        return s
%>\
from enum import Enum

__all__ = ['SLSCErrors', 'SLSCWarnings']

class SLSCErrors(Enum):
%for error in errors:
% if error['code'] < 0:
    ${remove_k_prefix(convert_to_snake_case(error['symbol']).upper())} = ${error['code']}
% endif
%endfor

class SLSCWarnings(Enum):
%for error in errors:
% if error['code'] > 0:
    ${remove_k_prefix(convert_to_snake_case(error['symbol']).upper())} = ${error['code']}
% endif
%endfor