"""Utility functions for the interpreter code generation process.

These functions help with converting names, determining parameter types,
and handling data types in the context of generating C API bindings for
the NI-SLSC API.
"""

import re

INTERPRETER_CAMEL_TO_SNAKE_CASE_REGEXES = [
    re.compile("([^_\n])([A-Z][a-z]+)"),
    re.compile("([a-z])([A-Z])"),
    re.compile("([0-9])([^_0-9])"),
]

NAME_EXPANSION = {
    "chassis": "chassisName",
    "device": "deviceName",
    "devices": "deviceNames",
    "library": "libraryHandle",
    "nvmemAreas": "nvmemAreaNames",
    "physChan": "physicalChannelNames",
    "physChans": "physicalChannelNames",
    "session": "sessionHandle",
    "property": "propertyName",
    "propertyIn": "propertyName",
    "command": "commandName",
    "commandIn": "commandName",
    "commandRef": "commandHandle",
    "commandRefOut": "commandHandle",
    "propertyRef": "propertyHandle",
    "propertyRefOut": "propertyHandle",
}

CLASSNAME_MAP = {
    "Session": "Session",
    "Library": "Library",
    "CommandReference": "Command",
    "PropertyReference": "Property",
}

DATATYPE_MAP = {
    "uint8": "ctypes.c_uint8",
    "uint16": "ctypes.c_uint16",
    "uint32": "ctypes.c_uint32",
    "int32": "ctypes.c_int32",
    "uint64": "ctypes.c_uint64",
    "int64": "ctypes.c_int64",
    "double": "ctypes.c_double",
    "bool": "ctypes.c_bool",
    "string": "ctypes.c_char_p",
    "Library": "ctypes.c_void_p",
    "Session": "ctypes.c_void_p",
    "Device": "ctypes.c_char_p",
    "PhysChan": "ctypes.c_char_p",
    "NvmemArea": "ctypes.c_char_p",
    "Property": "ctypes.c_char_p",
    "Command": "ctypes.c_char_p",
    "CommandReference": "ctypes.c_void_p",
    "TimeoutSeconds": "ctypes.c_double",
    "Status": "ctypes.c_int32",
    "PropertyReference": "ctypes.c_void_p",
    "string[]": "ctypes.c_char_p",
    "double[]": "ctypes.c_double",
    "int64[]": "ctypes.c_int64",
    "uint64[]": "ctypes.c_uint64",
    "int32[]": "ctypes.c_int32",
    "uint32[]": "ctypes.c_uint32",
    "uint8[]": "ctypes.c_uint8",
    "bool[]": "ctypes.c_bool",
    "enum": "ctypes.c_int32",
}


def convert_to_snake_case(name: str) -> str:
    """Convert a camelCase or PascalCase name to snake_case."""
    for regex in INTERPRETER_CAMEL_TO_SNAKE_CASE_REGEXES:
        name = regex.sub(r"\1_\2", name)
    return name.lower().replace("u_int", "uint")


def convert_to_class_name(name: str) -> str:
    """Convert a property to its corresponding class name."""
    return CLASSNAME_MAP.get(name)


def is_param_input(param: dict) -> bool:
    """Check if the parameter is an input parameter."""
    return "in" in param["dir"]


def is_param_output(param: dict) -> bool:
    """Check if the parameter is an output parameter."""
    return "out" in param["dir"]


def is_capi(param: dict) -> bool:
    """Check if the parameter is part of the C API."""
    return "targets" not in param or "capi" in param["targets"]


def get_standardized_param_name(param: dict) -> str:
    """Get the standardized parameter name, expanding known names."""
    return convert_to_snake_case(NAME_EXPANSION.get(param["name"], param["name"]))


def get_param_datatype_in_ctypes(param: dict) -> str:
    """Get the ctypes equivalent of the parameter's data type."""
    if param["dataType"] not in DATATYPE_MAP:
        raise ValueError(f"Unknown dataType: {param['dataType']}")
    return DATATYPE_MAP[param["dataType"]]


def get_capi_function_name(function: dict) -> str:
    """Get the C API function name, using 'capiname' if available."""
    if "capi" in function["targets"]:
        if "capiname" in function:
            return function["capiname"]
    return function["name"]


def get_python_function_name(function: dict) -> str:
    """Get the Python function name, converting to snake_case."""
    if "capi" in function["targets"]:
        if "capiname" in function:
            return convert_to_snake_case(function["capiname"])
    return convert_to_snake_case(function["name"])
