from nislsc.constants import DataType
from nislsc.session import Session
from typing import Any

def get_property(session: Session, resource: str, property: str, datatype: DataType) -> Any:
    """Retrieve the current value of a property based on its data type."""
    if datatype == DataType.BOOL:
        return session.get_generic_property_bool(resource, property)
    elif datatype == DataType.DOUBLE:
        return session.get_generic_property_double(resource, property)
    elif datatype == DataType.INT32:
        return session.get_generic_property_int32(resource, property)
    elif datatype == DataType.INT64:
        return session.get_generic_property_int64(resource, property)
    elif datatype == DataType.STRING:
        return session.get_generic_property_string(resource, property)
    elif datatype == DataType.UINT32:
        return session.get_generic_property_uint32(resource, property)
    elif datatype == DataType.UINT64:
        return session.get_generic_property_uint64(resource, property)
    elif datatype == DataType.BOOL_ARRAY:
        return session.get_generic_property_bool_array(resource, property)
    elif datatype == DataType.DOUBLE_ARRAY:
        return session.get_generic_property_double_array(resource, property)
    elif datatype == DataType.INT32_ARRAY:
        return session.get_generic_property_int32_array(resource, property)
    elif datatype == DataType.INT64_ARRAY:
        return session.get_generic_property_int64_array(resource, property)
    elif datatype == DataType.STRING_ARRAY:
        return session.get_generic_property_string_array(resource, property)
    elif datatype == DataType.UINT32_ARRAY:
        return session.get_generic_property_uint32_array(resource, property)
    elif datatype == DataType.UINT64_ARRAY:
        return session.get_generic_property_uint64_array(resource, property)
    else:
        return "Unsupported DataType"
