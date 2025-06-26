<%!
    from utilities.interpreter_helpers import convert_to_snake_case

    def remove_k_prefix(s: str) -> str:
        if s.upper().startswith("K_"):
            return s[2:]
        return s
%>\
from enum import Enum

__all__ = ['ErrorCode']

class ErrorCode(Enum):
    SUCCESS = 0
%for error in errors:
    ${remove_k_prefix(convert_to_snake_case(error['symbol']).upper())} = ${error['code']}
%endfor