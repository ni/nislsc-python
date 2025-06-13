import copy
import re
import sys
from utilities.enum_helpers import NAME_EXPANSION, DIR_MAPPING, CHAR_LIST, IN_DIR_MAPPING, OUT_DIR_MAPPING, VOID_LIST

INTERPRETER_CAMEL_TO_SNAKE_CASE_REGEXES = [
    re.compile("([^_\n])([A-Z][a-z]+)"),
    re.compile("([a-z])([A-Z])"),
    re.compile("([0-9])([^_0-9])"),
]
    
ARRAY_VAR = [
    "int64[]", "uint64[]", "int32[]", "uint32[]", "bool[]", "double[]"
]

# Previous used to list all the parameters when pythonic is not being considered
def list_all_variable(param):
    name = std_var_name(param)
    if 'out' in param['dir']:
        if param['dataType'] == 'string' or param['dataType'] == 'Device':
            name = f"{name}, {name}Size, {name}ActualSize"
        elif param['dataType'] == 'string[]':
                name = f"{name}, numberOf_{name}, buffer, bufferSize, requiredBufferSize"
        elif param['dataType'] in ARRAY_VAR:
            name = f"{name}, {name}ArraySize, {name}ArrayActualSize"
        elif param['dataType'] == 'uint8[]':
            name = f"{name}, {name}ArraySize"
    elif 'in' in param['dir']:
        if param['dataType'] == 'string[]':
            if name == 'namesIn':
                name = f"{name}, {name}Size"
            else:
                name = f"{name}, {name}ArraySize"
        elif param['dataType'] in ARRAY_VAR or param['dataType'] == 'uint8[]':
            name = f"{name}, {name}ArraySize"

    return convert(name)

# convert name to snake casing
def convert(name):
    for regex in INTERPRETER_CAMEL_TO_SNAKE_CASE_REGEXES:
        name = regex.sub(r"\1_\2", name)
    return name.lower().replace("_u_int", "_uint")

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

# argument parameter placeholder
def arg_placeholder(function):
    arg_list = []
    if 'capi' in function['targets']:
        for parameter in function['params']:
            if is_capi(parameter) and is_dir_in(parameter):
                arg_list.append(IN_DIR_MAPPING.get(parameter['dataType'], "Error_in_INPUT"))
            elif is_capi(parameter) and is_dir_out(parameter):
                arg_list.append(OUT_DIR_MAPPING.get(parameter['dataType'], "Error_in_OUTPUT"))
    return arg_list

# standard function name
def std_func_name(function):
    if 'capi' in function["targets"]:
        if 'capiname' in function:
            return convert(function['capiname'])
    return convert(function['name'])

# C function name
def c_func_name(function):
    if 'capi' in function["targets"]:
        if 'capiname' in function:
            return function['capiname']
    return function['name']


# parameter placeholder
def param_placeholder(function):
    param_list = []
    if 'capi'in function['targets']:
        for parameter in function['params']:
            if is_capi(parameter) and is_dir_in(parameter) and 'Size' not in parameter['name']: 
                if parameter['dataType'] == 'uint8[]' and parameter['name'] == 'byte':
                    param_list.append(f"{std_var_name(parameter)}s_data")
                else:
                    param_list.append(std_var_name(parameter))
            elif is_capi(parameter) and is_dir_out(parameter) and parameter['dataType'] == 'uint8[]':
                param_list.append(f"num_{std_var_name(parameter)}")  
    return param_list

# variable specification
def var_spec(function):
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):   
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{std_var_name(parameter)} = ctypes.POINTER({var_mapping(parameter)})()")
                    var_list.append(f"num_{std_var_name(parameter)} = ctypes.c_size_t()")
                    var_list.append(f"required_buffer_size = ctypes.c_size_t()")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{std_var_name(parameter)}_actual_size = ctypes.c_size_t()")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{std_var_name(parameter)}_array = ({var_mapping(parameter)} * num_{std_var_name(parameter)})()")
            else:
                if parameter['dataType'] not in CHAR_LIST:
                    var_list.append(f"{std_var_name(parameter)} = {var_mapping(parameter)}()")
                else:
                    var_list.append(f"{std_var_name(parameter)}_actual_size = ctypes.c_size_t()")
        elif is_capi(parameter) and is_dir_in(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{std_var_name(parameter)} = [string.encode('utf-8') for string in {std_var_name(parameter)}]")
                    var_list.append(f"array_type = {var_mapping(parameter)} * len({std_var_name(parameter)})")
                    var_list.append(f"{std_var_name(parameter)}_array = array_type(*{std_var_name(parameter)})")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{std_var_name(parameter)}_array = ({var_mapping(parameter)} * len({std_var_name(parameter)}))(*{std_var_name(parameter)})")
                    var_list.append(f"{std_var_name(parameter)}_array_size = len({std_var_name(parameter)})")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{std_var_name(parameter)}_array_size = len({std_var_name(parameter)}s_data)")
                    var_list.append(f"{std_var_name(parameter)}_array = ({var_mapping(parameter)} * {std_var_name(parameter)}_array_size)(*{std_var_name(parameter)}s_data)")
            else:
                if parameter['dataType'] in CHAR_LIST:
                    var_list.append(f"{std_var_name(parameter)} = {std_var_name(parameter)}.encode('utf-8')")
                else:
                    var_list.append(f"{std_var_name(parameter)} = {var_mapping(parameter)}({std_var_name(parameter)})")

    return var_list

# function parameter to find the size value           
def size_call(function):
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"ctypes.byref({std_var_name(parameter)})")
                    var_list.append(f"ctypes.byref(num_{std_var_name(parameter)})")
                    var_list.append(f"None")
                    var_list.append(f"0")
                    var_list.append(f"ctypes.byref(required_buffer_size)")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"None")
                    var_list.append(f"0")
                    var_list.append(f"ctypes.byref({std_var_name(parameter)}_actual_size)")
            elif parameter['dataType'] in CHAR_LIST:
                var_list.append(f"None")
                var_list.append(f"0")
                var_list.append(f"ctypes.byref({std_var_name(parameter)}_actual_size)")

        elif is_capi(parameter) and is_dir_in(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{std_var_name(parameter)}_array")
                    var_list.append(f"ctypes.c_size_t(len({std_var_name(parameter)}))")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"ctypes.byref({std_var_name(parameter)}_array)")
                    var_list.append(f"{std_var_name(parameter)}_array_size")
            else:
                var_list.append(f"{std_var_name(parameter)}")

    return var_list

# function call parameter
def func_call(function):
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"ctypes.byref({std_var_name(parameter)})")
                    var_list.append(f"ctypes.byref(num_{std_var_name(parameter)})")
                    var_list.append(f"buffer")
                    var_list.append(f"required_buffer_size.value")
                    var_list.append(f"None")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{std_var_name(parameter)}")
                    var_list.append(f"{std_var_name(parameter)}_actual_size.value")
                    var_list.append(f"None")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{std_var_name(parameter)}_array")
                    var_list.append(f"num_{std_var_name(parameter)}")
            else:
                if parameter['dataType'] in CHAR_LIST:
                    var_list.append(f"buffer")
                    var_list.append(f"{std_var_name(parameter)}_actual_size.value")
                    var_list.append(f"None")
                else:
                    var_list.append(f"ctypes.byref({std_var_name(parameter)})")

        elif is_capi(parameter) and is_dir_in(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{std_var_name(parameter)}_array")
                    var_list.append(f"ctypes.c_size_t(len({std_var_name(parameter)}))")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{std_var_name(parameter)}_array")
                    var_list.append(f"{std_var_name(parameter)}_array_size")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{std_var_name(parameter)}_array")
                    var_list.append(f"{std_var_name(parameter)}_array_size")
            else:
                var_list.append(f"{std_var_name(parameter)}")

    return var_list

# additional declaration between function calls
def add_decl(function):
    decl_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    decl_list.append(f"buffer = ctypes.create_string_buffer(required_buffer_size.value)")
                else:
                    decl_list.append(f"{std_var_name(parameter)} = ({var_mapping(parameter)} * {std_var_name(parameter)}_actual_size.value)()")
            elif parameter['dataType'] in CHAR_LIST:
                decl_list.append(f"buffer = ctypes.create_string_buffer({std_var_name(parameter)}_actual_size.value)")

    return decl_list

# required size checker
def req_size(function):
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if ('[]' in parameter['dataType'] and 'uint8[]' not in parameter['dataType']) or parameter['dataType'] in CHAR_LIST:
                return True
    return False

# convert result to pythonic format
def convert_res(function):
    conv_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    conv_list.append(f"{std_var_name(parameter)}_array = []")
                    conv_list.append(f"for i in range(num_{std_var_name(parameter)}.value):")
                    conv_list.append(f"    {std_var_name(parameter)}_array.append(ctypes.string_at({std_var_name(parameter)}[i]).decode('utf-8'))")
                elif parameter['dataType'] in ARRAY_VAR:
                    conv_list.append(f"{std_var_name(parameter)}_array = [{std_var_name(parameter)}[i] for i in range({std_var_name(parameter)}_actual_size.value)]")
            else:
                if parameter['dataType'] in CHAR_LIST:
                    conv_list.append(f"{std_var_name(parameter)}_value = buffer.value.decode('utf-8')")
    return conv_list

# return parameter for function
def return_param(function):
    ret_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] != 'uint8[]':
                    ret_list.append(f"{std_var_name(parameter)}_array")
                else:
                    ret_list.append(f"bytes({std_var_name(parameter)}_array)")
            else:
                if parameter['dataType'] in CHAR_LIST:
                    ret_list.append(f"{std_var_name(parameter)}_value")
                else:
                    ret_list.append(f"{std_var_name(parameter)}.value")

    return ret_list
    
