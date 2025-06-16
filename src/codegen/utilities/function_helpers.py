from utilities.interpreter_helpers import is_capi, is_dir_in, is_dir_out, std_var_name, var_mapping

ARRAY_VAR = [
    "int64[]", "uint64[]", "int32[]", "uint32[]", "bool[]", "double[]"
]

CHAR_LIST = {
    "string": "ctypes.c_char_p",
    "Device": "ctypes.c_char_p",
    "PhysChan": "ctypes.c_char_p",
    "NvmemArea": "ctypes.c_char_p",
    "Property": "ctypes.c_char_p",
    "Command": "ctypes.c_char_p",
}

# function header argument placeholder
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

# specifies the variable declaration for the function
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

# call this function to get the size needed for the return value    
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

# additional variable declaration to create buffers
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

# call function with complete parameters
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

# checks if the function needs additional function call to determine size of the return value
def req_size(function):
    for parameter in function['params']:
        if is_capi(parameter) and is_dir_out(parameter):
            if ('[]' in parameter['dataType'] and 'uint8[]' not in parameter['dataType']) or parameter['dataType'] in CHAR_LIST:
                return True
    return False

# produce conversion method for return values
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

# create the return parameter for the function
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