<%!
    from utilities.interpreter_helpers import convert
%>\
from enum import IntEnum

% for enum in enums:
% if 'capi' in enum['targets']:
class ${enum['name']}(IntEnum):
% for value in enum['values']:
% if 'internal' not in value:
    NISLSC_${convert(enum['name']).upper()}_${convert(value['name']).upper()} = ${value['value']}
% endif
% endfor

% endif
% endfor