"""Assist example scripts with common utility functions.

This module provides helper functions for SLSC example scripts, enabling
dynamic property retrieval.
"""

from nislsc.constants import DataType
from nislsc.session import Session
from typing import Any

def _get_session_generic_property(session: Session, resource: str, property: str, datatype: DataType) -> Any:
    """Retrieve the current value of a property based on its data type.
    
    Args:
        session: SLSC session instance.
        resource: Device or physical channel name.
        property: Property name to retrieve.
        datatype: DataType enum indicating the property's data type.
    
    Returns:
        Property value in its native type, or "Unsupported DataType" if invalid.  
    """
    if 1 <= datatype.value <= 14:
        method_name = f"get_generic_property_{datatype.name.lower()}"
        method = getattr(session, method_name)
        return method(resource, property)
    else:
        return "Unsupported DataType"