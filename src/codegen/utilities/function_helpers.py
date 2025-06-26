from utilities.interpreter_helpers import is_capi, is_param_input, is_param_output, get_standardized_param_name, get_param_datatype_in_ctypes

ARRAY_VAR = [
    "int64[]", "uint64[]", "int32[]", "uint32[]", "bool[]", "double[]"
]

STRING_LIST = {
    "string": "ctypes.c_char_p",
    "Device": "ctypes.c_char_p",
    "PhysChan": "ctypes.c_char_p",
    "NvmemArea": "ctypes.c_char_p",
    "Property": "ctypes.c_char_p",
    "Command": "ctypes.c_char_p",
}

PYTHON_DATATYPE_MAP= {
    "uint8": "int",
    "uint16": "int",
    "uint32": "int",
    "int32": "int",
    "uint64": "int",
    "int64": "int",
    "double": "float",
    "bool": "bool",
    "string": "str",
    "Library": "int",
    "Session": "int",
    "Device": "str",
    "PhysChan": "str",
    "NvmemArea": "str",
    "Property": "str",
    "Command": "str",
    "CommandReference": "int",
    "TimeoutSeconds": "float",
    "Status": "int",
    "PropertyReference": "int",
    "string[]": "list[str]",
    "double[]": "list[float]",
    "int64[]": "list[int]",
    "uint64[]": "list[int]",
    "int32[]": "list[int]",
    "uint32[]": "list[int]",
    "uint8[]": "bytes",
    "bool[]": "list[bool]",
    "enum": "int"
}


INPUT_DATATYPE_MAP = {
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
    "string[]": "ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t",
    "double[]": "ctypes.POINTER(ctypes.c_double), ctypes.c_size_t",
    "int64[]": "ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t",
    "uint64[]": "ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t",
    "int32[]": "ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t",
    "uint32[]": "ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t",
    "uint8[]": "ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t",
    "bool[]": "ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t",
    "enum": "ctypes.c_int32"
}

OUTPUT_DATATYPE_MAP = {
    "uint8": "ctypes.POINTER(ctypes.c_uint8)",
    "uint16": "ctypes.POINTER(ctypes.c_uint16)",
    "uint32": "ctypes.POINTER(ctypes.c_uint32)",
    "int32": "ctypes.POINTER(ctypes.c_int32)",
    "uint64": "ctypes.POINTER(ctypes.c_uint64)",
    "int64": "ctypes.POINTER(ctypes.c_int64)",
    "double": "ctypes.POINTER(ctypes.c_double)",
    "bool": "ctypes.POINTER(ctypes.c_bool)",
    "string": "ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "Library": "ctypes.POINTER(ctypes.c_void_p)",
    "Session": "ctypes.POINTER(ctypes.c_void_p)",
    "Device": "ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "CommandReference": "ctypes.POINTER(ctypes.c_void_p)",
    "PropertyReference": "ctypes.POINTER(ctypes.c_void_p)",
    "string[]": "ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "double[]": "ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "int64[]": "ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "uint64[]": "ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "int32[]": "ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "uint32[]": "ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "uint8[]": "ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t",
    "bool[]": "ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)",
    "enum": "ctypes.POINTER(ctypes.c_int32)"
}

def get_ctypes_argtypes(function: dict) -> list[str]:
    arg_list = []
    if 'capi' in function['targets']:
        for parameter in function['params']:
            if is_capi(parameter) and is_param_input(parameter):
                if parameter['dataType'] not in INPUT_DATATYPE_MAP:
                    raise ValueError(f"Unknown input dataType: {parameter['dataType']}")
                arg_list.append(INPUT_DATATYPE_MAP[parameter['dataType']])
            elif is_capi(parameter) and is_param_output(parameter):
                if parameter['dataType'] not in OUTPUT_DATATYPE_MAP:
                    raise ValueError(f"Unknown output dataType: {parameter['dataType']}")
                arg_list.append(OUTPUT_DATATYPE_MAP[parameter['dataType']])
    return arg_list

def get_function_parameter_list(function: dict) -> list[str]:
    param_list = ['self']
    if 'capi'in function['targets']:
        for parameter in function['params']:
            if is_capi(parameter) and is_param_input(parameter) and 'Size' not in parameter['name']: 
                if parameter['dataType'] == 'uint8[]':
                    param_list.append(f"{get_standardized_param_name(parameter)}s_data: bytes")
                else:
                    param_list.append(f"{get_standardized_param_name(parameter)}: {PYTHON_DATATYPE_MAP.get(parameter['dataType'])}")
            elif is_capi(parameter) and is_param_output(parameter) and parameter['dataType'] == 'uint8[]':
                param_list.append(f"num_{get_standardized_param_name(parameter)}: int") 
    return param_list

def get_function_return_type(function: dict) -> str:
    if 'capi' in function['targets']:
        param_list = []
        num = 0
        for parameter in function['params']:
            if is_capi(parameter) and is_param_output(parameter):
                param_list.append(f"{PYTHON_DATATYPE_MAP.get(parameter['dataType'])}")
                num += 1
    if num == 0:
        return " -> None"
    elif num == 1:
        return f" -> {param_list[0]}"
    else:
        return f" -> tuple[{', '.join(param_list)}]"
                
# specifies the variable declaration for the function
def generate_variable_declaration(function: dict) -> list[str]:
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):   
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{get_standardized_param_name(parameter)} = ctypes.POINTER({get_param_datatype_in_ctypes(parameter)})()")
                    var_list.append(f"num_{get_standardized_param_name(parameter)} = ctypes.c_size_t()")
                    var_list.append(f"required_buffer_size = ctypes.c_size_t()")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{get_standardized_param_name(parameter)}_actual_size = ctypes.c_size_t()")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{get_standardized_param_name(parameter)}_array = ({get_param_datatype_in_ctypes(parameter)} * num_{get_standardized_param_name(parameter)})()")
            else:
                if parameter['dataType'] not in STRING_LIST:
                    var_list.append(f"{get_standardized_param_name(parameter)} = {get_param_datatype_in_ctypes(parameter)}()")
                else:
                    var_list.append(f"{get_standardized_param_name(parameter)}_actual_size = ctypes.c_size_t()")
        elif is_capi(parameter) and is_param_input(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{get_standardized_param_name(parameter)} = [string.encode('utf-8') for string in {get_standardized_param_name(parameter)}]")
                    var_list.append(f"array_type = {get_param_datatype_in_ctypes(parameter)} * len({get_standardized_param_name(parameter)})")
                    var_list.append(f"{get_standardized_param_name(parameter)}_array = array_type(*{get_standardized_param_name(parameter)})")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{get_standardized_param_name(parameter)}_array = ({get_param_datatype_in_ctypes(parameter)} * len({get_standardized_param_name(parameter)}))(*{get_standardized_param_name(parameter)})")
                    var_list.append(f"{get_standardized_param_name(parameter)}_array_size = len({get_standardized_param_name(parameter)})")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{get_standardized_param_name(parameter)}_array_size = len({get_standardized_param_name(parameter)}s_data)")
                    var_list.append(f"{get_standardized_param_name(parameter)}_array = ({get_param_datatype_in_ctypes(parameter)} * {get_standardized_param_name(parameter)}_array_size)(*{get_standardized_param_name(parameter)}s_data)")
            else:
                if parameter['dataType'] in STRING_LIST:
                    var_list.append(f"{get_standardized_param_name(parameter)} = {get_standardized_param_name(parameter)}.encode('utf-8')")
                else:
                    var_list.append(f"{get_standardized_param_name(parameter)} = {get_param_datatype_in_ctypes(parameter)}({get_standardized_param_name(parameter)})")
    return var_list

# call this function to get the size needed for the return value    
def generate_function_call_for_size(function: dict) -> list[str]:
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"ctypes.byref({get_standardized_param_name(parameter)})")
                    var_list.append(f"ctypes.byref(num_{get_standardized_param_name(parameter)})")
                    var_list.append(f"None")
                    var_list.append(f"0")
                    var_list.append(f"ctypes.byref(required_buffer_size)")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"None")
                    var_list.append(f"0")
                    var_list.append(f"ctypes.byref({get_standardized_param_name(parameter)}_actual_size)")
            elif parameter['dataType'] in STRING_LIST:
                var_list.append(f"None")
                var_list.append(f"0")
                var_list.append(f"ctypes.byref({get_standardized_param_name(parameter)}_actual_size)")

        elif is_capi(parameter) and is_param_input(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{get_standardized_param_name(parameter)}_array")
                    var_list.append(f"ctypes.c_size_t(len({get_standardized_param_name(parameter)}))")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"ctypes.byref({get_standardized_param_name(parameter)}_array)")
                    var_list.append(f"{get_standardized_param_name(parameter)}_array_size")
            else:
                var_list.append(f"{get_standardized_param_name(parameter)}")

    return var_list

# call this function to generate validation  
def generate_function_call_validation(function: dict) -> str:
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if parameter['dataType'] == 'string[]':
                var_list.append("required_buffer_size.value <= 0")
            else:
                var_list.append(f"{get_standardized_param_name(parameter)}_actual_size.value <= 0")
    return " or ".join(var_list)

# additional variable declaration to create buffers
def generate_additional_variable_declaration(function: dict) ->  list[str]:
    decl_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    decl_list.append(f"buffer = ctypes.create_string_buffer(required_buffer_size.value)")
                else:
                    decl_list.append(f"{get_standardized_param_name(parameter)} = ({get_param_datatype_in_ctypes(parameter)} * {get_standardized_param_name(parameter)}_actual_size.value)()")
            elif parameter['dataType'] in STRING_LIST:
                decl_list.append(f"buffer = ctypes.create_string_buffer({get_standardized_param_name(parameter)}_actual_size.value)")

    return decl_list

# call function with complete parameters
def generate_function_call_for_result(function: dict) -> list[str]:
    var_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"ctypes.byref({get_standardized_param_name(parameter)})")
                    var_list.append(f"ctypes.byref(num_{get_standardized_param_name(parameter)})")
                    var_list.append(f"buffer")
                    var_list.append(f"required_buffer_size.value")
                    var_list.append(f"None")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{get_standardized_param_name(parameter)}")
                    var_list.append(f"{get_standardized_param_name(parameter)}_actual_size.value")
                    var_list.append(f"None")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{get_standardized_param_name(parameter)}_array")
                    var_list.append(f"num_{get_standardized_param_name(parameter)}")
            else:
                if parameter['dataType'] in STRING_LIST:
                    var_list.append(f"buffer")
                    var_list.append(f"{get_standardized_param_name(parameter)}_actual_size.value")
                    var_list.append(f"None")
                else:
                    var_list.append(f"ctypes.byref({get_standardized_param_name(parameter)})")

        elif is_capi(parameter) and is_param_input(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    var_list.append(f"{get_standardized_param_name(parameter)}_array")
                    var_list.append(f"ctypes.c_size_t(len({get_standardized_param_name(parameter)}))")
                elif parameter['dataType'] in ARRAY_VAR:
                    var_list.append(f"{get_standardized_param_name(parameter)}_array")
                    var_list.append(f"{get_standardized_param_name(parameter)}_array_size")
                elif parameter['dataType'] == 'uint8[]':
                    var_list.append(f"{get_standardized_param_name(parameter)}_array")
                    var_list.append(f"{get_standardized_param_name(parameter)}_array_size")
            else:
                var_list.append(f"{get_standardized_param_name(parameter)}")

    return var_list

# checks if the function needs additional function call to determine size of the return value
def is_size_unknown(function: dict) -> bool:
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if ('[]' in parameter['dataType'] and 'uint8[]' not in parameter['dataType']) or parameter['dataType'] in STRING_LIST:
                return True
    return False

# produce conversion method for return values
def generate_result_parser(function: dict) -> list[str]:
    conv_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] == 'string[]':
                    conv_list.append(f"{get_standardized_param_name(parameter)}_array = []")
                    conv_list.append(f"for i in range(num_{get_standardized_param_name(parameter)}.value):")
                    conv_list.append(f"    {get_standardized_param_name(parameter)}_array.append(ctypes.string_at({get_standardized_param_name(parameter)}[i]).decode('utf-8'))")
                elif parameter['dataType'] in ARRAY_VAR:
                    conv_list.append(f"{get_standardized_param_name(parameter)}_array = [{get_standardized_param_name(parameter)}[i] for i in range({get_standardized_param_name(parameter)}_actual_size.value)]")
            else:
                if parameter['dataType'] in STRING_LIST:
                    conv_list.append(f"{get_standardized_param_name(parameter)}_value = buffer.value.decode('utf-8')")
    return conv_list

# create the return parameter for the function
def generate_return_parameter(function: dict) -> list[str]:
    ret_list = []
    for parameter in function['params']:
        if is_capi(parameter) and is_param_output(parameter):
            if '[]' in parameter['dataType']:
                if parameter['dataType'] != 'uint8[]':
                    ret_list.append(f"{get_standardized_param_name(parameter)}_array")
                else:
                    ret_list.append(f"bytes({get_standardized_param_name(parameter)}_array)")
            else:
                if parameter['dataType'] in STRING_LIST:
                    ret_list.append(f"{get_standardized_param_name(parameter)}_value")
                else:
                    ret_list.append(f"{get_standardized_param_name(parameter)}.value")

    return ret_list

def has_library_handle(function: dict) -> str:
    for parameter in function['params']:
        if is_capi(parameter) and is_param_input(parameter) and parameter['dataType'] == 'Library':
            return "library_handle.value"
    return "None"