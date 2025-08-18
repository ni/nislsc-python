"""Generate docstrings for code generation.

These functions help generate properly wrapped and formatted docstrings for the
generated Python API, including argument and return descriptions, and handling
specific data types.
"""

import re
import textwrap

from utilities.interpreter_helpers import (
    get_standardized_param_name,
    is_capi,
    is_param_input,
    is_param_output,
)

INDENTATION = "    "

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


def generate_docstrings(
    function: dict, ignore_type: str = "", is_classmethod: bool = False
) -> list[str]:
    """Generate a Google style docstring for a function."""
    docstrings = []
    for doc in generate_doc(function):
        docstrings.append(doc)
    if len(generate_args(function, ignore_type, is_classmethod)) != 0:
        docstrings.append("")
        for arg in generate_args(function, ignore_type, is_classmethod):
            docstrings.append(arg)
    if len(generate_returns(function)) != 0:
        docstrings.append("")
        for ret in generate_returns(function):
            docstrings.append(ret)

    for i, line in enumerate(docstrings):
        if "\\" in line:
            docstrings[i] = re.sub(r"\\", r"\\\\", line)

    docstrings[0] = '"""' + docstrings[0]
    if len(docstrings) == 1:
        docstrings[0] = docstrings[0] + '"""'
    else:
        docstrings.append('"""')

    wrapped_docstrings = []
    for line in docstrings:
        if line == "":
            wrapped_docstrings.append("")
            continue

        subsequent_indent = ""
        if line.startswith(INDENTATION):
            subsequent_indent = f"{INDENTATION}{INDENTATION}"
        elif line.startswith("-"):
            subsequent_indent = "  "
        wrapped_line = textwrap.wrap(line, width=72, subsequent_indent=subsequent_indent)
        wrapped_docstrings.extend(wrapped_line)

    return wrapped_docstrings


def generate_doc(function: dict) -> list[str]:
    """Generate the summary and description part of the docstring."""
    doc = []
    first_split = function["doc"].split(".", 1)
    first_sentence = first_split[0] + "."
    words = first_sentence.split()
    first_word = IMPERATIVE_DOCSTRINGS_MAP.get(words[0], "Error")
    new_sentence = first_word + " " + " ".join(words[1:])
    doc.append(new_sentence)
    if len(first_split[1]) != 0:
        rest_sentence = first_split[1].strip()
        doc_lines = rest_sentence.split("\n\n")
        for text in doc_lines:
            doc.append("")
            doc.append(text)
    return doc


def generate_args(function: dict, ignore_type: str, is_classmethod: bool = False) -> list[str]:
    """Generate the Args section of the docstring."""
    args = []
    if is_inputting_something(function, ignore_type):
        args.append("Args:")
    for param in function["params"]:
        if is_capi(param) and is_param_input(param):
            if param["dataType"] == ignore_type:
                continue
            elif param["dataType"] == "Library" and is_classmethod:
                args_line = "library: Previously initialized Library instance."
            elif param["dataType"] == "Session" and is_classmethod:
                args_line = "session: Previously initialized Session instance."
            else:
                args_line = f"{get_standardized_param_name(param)}: {param['doc']}"
                if not args_line.endswith("."):
                    args_line = args_line + "."
            args.append(f"{INDENTATION}{args_line}")
    return args


def generate_returns(function: dict) -> list[str]:
    """Generate the Returns section of the docstring."""
    returns = []
    ret_line = []
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
                ret_line.append("New instance of " + param["dataType"] + " object")
            else:
                if param["doc"].endswith("."):
                    ret_line.append(f"{param['doc'][:-1]}".lower())
                else:
                    ret_line.append(f"{param['doc']}".lower())
    if len(ret_line) == 1:
        one_line = ret_line[0]
        if not one_line.endswith("."):
            one_line = one_line + "."

        if not one_line[0].isupper():
            one_line = one_line.capitalize()

        returns.append(f"{INDENTATION}{one_line}")

    elif len(ret_line) == 2:
        tuple_line = "A tuple containing " + ret_line[0] + " and " + ret_line[1] + "."
        returns.append(f"{INDENTATION}{tuple_line}")
    elif len(ret_line) > 2:
        tuple_line = "A tuple containing " + ", ".join(ret_line[:-1]) + " and " + ret_line[-1] + "."
        returns.append(f"{INDENTATION}{tuple_line}")

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
