"""Utility functions for generating Google style docstrings in code generation.

These functions help generate properly wrapped and formatted docstrings for the
generated Python API, including argument and return descriptions, and handling
specific data types.
"""

from utilities.function_helpers import PYTHON_DATATYPE_MAP
from utilities.interpreter_helpers import (
    get_standardized_param_name,
    is_capi,
    is_param_input,
    is_param_output,
)

CLASS_DOCSTRINGS_MAP = {
    "Library": "Library: An instance of the Library class.",
    "Session": "Session: An instance of the Session class.",
    "PropertyReference": "Property: An instance of the Property class.",
    "CommandReference": "Command: An instance of the Command class.",
}

IMPERATIVE_DOCSTRINGS_MAP = {
    "Gets": "Get",
    "Sets": "Set",
    "Executes": "Execute",
    "Commits": "Commit",
    "Writes": "Write",
    "Initializes": "Initialize",
    "Returns": "Return",
    "Attempts": "Attempt",
    "Deletes": "Delete",
    "Opens": "Open",
    "Closes": "Close",
    "Reserves": "Reserve",
    "Unreserves": "Unreserve",
    "Resets": "Reset",
    "Renames": "Rename",
    "Updates": "Update",
    "Connects": "Connect",
    "Removes": "Remove",
    "Reads": "Read",
}


def wrap_text(text: str, width: int = 72, indent: str = "    ", is_doc: bool = False) -> list[str]:
    """Wraps text at a given width."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if is_doc:
            current_indent = '"""' if len(lines) == 0 else ""
        else:
            current_indent = indent if len(lines) == 0 else indent + indent
        if len(current_line.lstrip()) + len(word) + len(current_indent) > width:
            lines.append(current_indent + current_line.rstrip())
            current_line = word + " "
        else:
            current_line += word + " "
    if current_line:
        if is_doc:
            current_indent = '"""' if len(lines) == 0 else ""
        else:
            current_indent = indent if len(lines) == 0 else indent + indent
        lines.append(current_indent + current_line.rstrip())
    return lines


def generate_docstrings(function: dict, ignore_type: str = "") -> list[str]:
    """Generate a Google style docstring for a function."""
    docstrings = []
    for doc in generate_doc(function):
        docstrings.append(doc)
    if len(generate_args(function, ignore_type)) != 0:
        docstrings.append("")
        for arg in generate_args(function, ignore_type):
            docstrings.append(arg)
    if len(generate_returns(function)) != 0:
        docstrings.append("")
        for ret in generate_returns(function):
            docstrings.append(ret)
    docstrings.append('"""')
    return docstrings


def generate_doc(function: dict) -> list[str]:
    """Generate the summary and description part of the docstring."""
    doc = []
    first_split = function["doc"].split(".", 1)
    first_sentence = first_split[0] + "."
    words = first_sentence.split()
    first_word = IMPERATIVE_DOCSTRINGS_MAP.get(words[0], "Error")
    new_sentence = first_word + " " + " ".join(words[1:])
    summary_wrapped = wrap_text(new_sentence, 72, "", True)
    doc.append(summary_wrapped[0])
    for line in summary_wrapped[1:]:
        doc.append(line)
    if len(first_split[1]) != 0:
        rest_sentence = first_split[1].strip()
        doc_lines = rest_sentence.split("\n\n")
        for text in doc_lines:
            doc.append("")
            line = wrap_text(text, 72, "")
            for line in wrap_text(text, 72, ""):
                doc.append(line)
    return doc


def generate_args(function: dict, ignore_type: str) -> list[str]:
    """Generate the Args section of the docstring."""
    args = []
    if is_inputting_something(function, ignore_type):
        args.append("Args:")
    for param in function["params"]:
        if is_capi(param) and is_param_input(param):
            if param["dataType"] == ignore_type:
                continue
            args_line = f"{get_standardized_param_name(param)}: {param['doc']}"
            for text in wrap_text(args_line, 72):
                args.append(text)
    return args


def generate_returns(function: dict) -> list[str]:
    """Generate the Returns section of the docstring."""
    returns = []
    if is_returning_something(function):
        returns.append("Returns:")
    for param in function["params"]:
        if is_capi(param) and is_param_output(param):
            ret_line = f"{get_standardized_param_name(param)}: {param['doc']}"
            for text in wrap_text(ret_line, 72):
                returns.append(text)
    return returns


def is_returning_something(function: dict) -> bool:
    """Check if the function returns something."""
    for param in function["params"]:
        if is_capi(param) and is_param_output(param):
            return True
    return False


def is_inputting_something(function: dict, ignore_type: str = "") -> bool:
    """Check if the function has input parameters (excluding ignore_type)."""
    for param in function["params"]:
        if is_capi(param) and is_param_input(param) and param["dataType"] != ignore_type:
            return True
    return False
