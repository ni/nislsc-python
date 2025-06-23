import copy
import re
import sys

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

DIR_MAPPING = {
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
    "enum": "ctypes.c_int32"
}

# convert name to snake casing
def convert(name):
    for regex in INTERPRETER_CAMEL_TO_SNAKE_CASE_REGEXES:
        name = regex.sub(r"\1_\2", name)
    return name.lower().replace("u_int", "uint")

# in direction checker
def is_dir_in(param):
    return 'in' in param['dir']

# out direction checker
def is_dir_out(param):
    return 'out' in param['dir']

# capi checker
def is_capi(param):
    return 'targets' not in param or 'capi' in param['targets']

# standard variable name
def std_var_name(param):
    return convert(NAME_EXPANSION.get(param['name'], param['name']))

# variable mapping to ctypes
def var_mapping(param):
    return DIR_MAPPING.get(param['dataType'], "Error_in_datatype")

# returns c library's function name
def c_func_name(function):
    if 'capi' in function["targets"]:
        if 'capiname' in function:
            return function['capiname']
    return function['name']

# standard function name
def std_func_name(function):
    if 'capi' in function["targets"]:
        if 'capiname' in function:
            return convert(function['capiname'])
    return convert(function['name'])



    
