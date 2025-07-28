"""Define SLSC constants and enumerations.

This module provides enumeration classes that define constants and
configuration values used throughout the SLSC API.
"""

from enum import Enum

class ReservationAccess(Enum):
    """Define SLSC reservation access modes."""

    NONE = 0
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = 3

class PropertyAccess(Enum):
    """Define SLSC property access permissions."""

    NONE = 0
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = 3

class DataType(Enum):
    """Specify SLSC data types and array variants."""

    NONE = 0
    BOOL = 1
    DOUBLE = 2
    INT32 = 3
    INT64 = 4
    STRING = 5
    UINT32 = 6
    UINT64 = 7
    BOOL_ARRAY = 8
    DOUBLE_ARRAY = 9
    INT32_ARRAY = 10
    INT64_ARRAY = 11
    STRING_ARRAY = 12
    UINT32_ARRAY = 13
    UINT64_ARRAY = 14

class TableScaleCoercion(Enum):
    """Control table scaling coercion behavior."""

    INTERPOLATE = 0
    ROUND_TO_NEAREST = 1
    STRICT = 2

class Language(Enum):
    """Specify language codes for localized messages."""

    UNDEFINED = -1
    CURRENT_THREAD_LOCALE = 0
    ENGLISH = 1033
    FRENCH = 1036
    GERMAN = 1031
    JAPANESE = 1041
    KOREAN = 1042
    SIMPLIFIED_CHINESE = 2052

class ProductCategory(Enum):
    """Identify SLSC product categories."""

    UNKNOWN = 0
    SLSC_CHASSIS = 1
    SLSC_MODULE = 2

