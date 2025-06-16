from utilities.interpreter_helpers import is_capi, is_dir_in, is_dir_out

IN_DIR_MAPPING = {
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

OUT_DIR_MAPPING = {
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