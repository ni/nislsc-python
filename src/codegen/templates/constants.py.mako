<%!
    from utilities.interpreter_helpers import convert_to_snake_case
%>\
from enum import Enum

% for enum in enums:
% if 'capi' in enum['targets']:
class ${enum['name']}(Enum):
% for value in enum['values']:
% if 'internal' not in value:
   ${convert_to_snake_case(value['name']).upper()} = ${value['value']}
% endif
% endfor

% endif
% endfor