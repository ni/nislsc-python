from utilities.interpreter_helpers import (
    get_standardized_param_name,
    is_capi,
    is_param_input,
    is_param_output,   
)

from utilities.function_helpers import PYTHON_DATATYPE_MAP

CLASS_DOCSTRINGS_MAP = {
    "Library": "Library: An instance of the Library class.",
    "Session": "Session: An instance of the Session class.",
    "PropertyReference": "Property: An instance of the Property class.",
    "CommandReference": "Command: An instance of the Command class.",
}

def wrap_text(text, width=72):
    """Wraps text."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(current_line.rstrip())
            current_line = "    " + word + " "
        else:
            current_line += word + " "
    if current_line:
        lines.append(current_line.rstrip())
    return lines


def generate_docstrings(function, ignore_type):
    docstrings = []
    for doc in generate_doc(function):
        docstrings.append(doc)
    if generate_args(function, ignore_type):
        docstrings.append("")
        for arg in generate_args(function, ignore_type):
            docstrings.append(arg)
    if generate_returns(function):
        docstrings.append("")
        for ret in generate_returns(function):
            docstrings.append(ret)
    docstrings.append('"""')
    return docstrings


def generate_doc(function):
    doc = []        
    doc_lines = function['doc'].splitlines()
    doc.append('"""' + doc_lines[0])
    for line in doc_lines[1:]:
        if line.strip() == "":
            doc.append("")
        else:
            for text in wrap_text(line, 72):
                doc.append(text)
    return doc


def generate_args(function, ignore_type):
    args = []
    if is_inputting_something(function, ignore_type):
        args.append("Args:")
    for param in function["params"]:
        if is_capi(param) and is_param_input(param):
            if param['dataType'] == ignore_type:
                continue
            args_line = (f"    {get_standardized_param_name(param)} ({PYTHON_DATATYPE_MAP.get(param['dataType'])}): {param['doc']}")
            for text in wrap_text(args_line, 72):
                args.append("    " + text)
    return args
    
def generate_returns(function):
    returns = []
    if is_returning_something(function):
        returns.append("Returns:")
    for param in function["params"]:
        if is_capi(param) and is_param_output(param):
            if param["dataType"] in (
                "Library",
                "Session",
                "CommandReference",
                "PropertyReference",
            ):
                ret_line = CLASS_DOCSTRINGS_MAP.get(param['dataType'])
            else:
                ret_line = (f"    {get_standardized_param_name(param)} ({PYTHON_DATATYPE_MAP.get(param['dataType'])}): {param['doc']}")
            for text in wrap_text(ret_line, 72):
                returns.append("    " + text)
    return returns

def is_returning_something(function):
    """Check if the function returns something."""
    for param in function["params"]:
        if is_capi(param) and is_param_output(param):
            return True
    return False

def is_inputting_something(function, ignore_type = None):
    """Check if the function returns something."""
    for param in function["params"]:
        if is_capi(param) and is_param_input(param) and param['dataType'] != ignore_type:
            return True
    return False
