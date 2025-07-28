<%!
from utilities.interpreter_helpers import convert_to_snake_case

def gen_docstrings(name: str) -> str:
    """Generate docstrings based on given name."""
    if name == "ReservationAccess":
        return "Define SLSC reservation access modes."
    elif name == "PropertyAccess":
        return "Define SLSC property access permissions."
    elif name == "DataType":
        return "Specify SLSC data types and array variants."
    elif name == "TableScaleCoercion":
        return "Control table scaling coercion behavior."
    elif name == "Language":
        return "Specify language codes for localized messages."
    elif name == "ProductCategory":
        return "Identify SLSC product categories."

%>\
"""Define SLSC constants and enumerations.

This module provides enumeration classes that define constants and
configuration values used throughout the SLSC API.
"""

from enum import Enum

% for enum in enums:
% if "capi" in enum["targets"]:
class ${enum["name"]}(Enum):
    """${gen_docstrings(enum["name"])}"""

%if enum["name"] == "Language":
    UNDEFINED = -1
% endif
% for value in enum["values"]:
% if "internal" not in value:
    ${convert_to_snake_case(value["name"]).upper()} = ${value["value"]}
% endif
% endfor

% endif
% endfor