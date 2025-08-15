<%!
import re

from utilities.interpreter_helpers import (
    convert_camel_pascal_to_snake_case,
    convert_to_screaming_snake_case,
    get_standardized_property_scope_name,
)

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

def classify_property_by_scope(props: list) -> dict:
    """Classify properties by their scope."""
    classified = {}
    for prop in props:
        if "targets" not in prop or "capi" in prop["targets"]:
            scope = get_standardized_property_scope_name(prop["scope"])
            classified[scope] = classified.get(scope, [])

            doc = prop.get("doc", "")
            if '"' in doc:
                doc = re.sub(r'\"(.*?)\"', r'``\1``', doc)

            classified[scope].append({
                "name": prop["name"],
                "description": prop.get("description", prop["name"]),
                "doc": doc,
            })
    return classified

%>\
"""Define SLSC constants and enumerations.

This module provides enumeration classes that define constants and
configuration values used throughout the SLSC API.
"""

from enum import Enum
from typing import TYPE_CHECKING

try:
    from enum import StrEnum  # Python 3.11+
except ImportError:
    if not TYPE_CHECKING:

        class StrEnum(str, Enum):
            """StrEnum fallback for Python versions < 3.11."""

% for enum in enums:
% if "capi" in enum["targets"]:

class ${enum["name"]}(Enum):
    """${gen_docstrings(enum["name"])}"""

% if enum["name"] == "Language":
    UNDEFINED = -1
% endif
% for value in enum["values"]:
% if "internal" not in value:
    ${convert_camel_pascal_to_snake_case(value["name"]).upper()} = ${value["value"]}
% endif
% endfor

% endif
% endfor

% for scope, props in classify_property_by_scope(properties).items():
class ${scope}Property(StrEnum):
    """Define SLSC ${scope} properties."""

% for prop in props:
    ${convert_to_screaming_snake_case(prop["description"])} = "${prop["name"]}"
% if prop["doc"]:
    """${prop["doc"]}"""
% endif
% endfor


% endfor
