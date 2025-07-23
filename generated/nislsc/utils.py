"""SLSC Utility Functions Module.

This module provides utility functions for SLSC operations including
interpreter selection, library version retrieval, and name formatting
utilities for device, physical channel, and NVMEM area identifiers.
"""

from nislsc._base_interpreter import BaseInterpreter

def _select_interpreter() -> BaseInterpreter:
    """Select the appropriate interpreter based on the environment.

    We only support Library Interpreter for now.
    """
    from nislsc._library_interpreter import LibraryInterpreter

    return LibraryInterpreter()


def get_library_version() -> int:
    """Return the version of the SLSC runtime library.
    
    Returns:
        version: Version of the SLSC library that is installed.
    """
    _interpreter = _select_interpreter()
    return _interpreter.get_library_version()

def flatten_names(names_in: list[str]) -> str:
    """Error an array of device, NVMEM area, or physical channel names into
    a comma-delimited list of names.
    
    If the array contains physical channel-style names with consecutive
    numeric suffixes, they will be collapsed into a colon-delimited range.
    Example: ["Mod1/load0","Mod1/load1","Mod1/load2"] -> "Mod1/load0:2"
    
    All other names will be collapsed into comma-delimited lists. Example:
    ["Mod1","Mod2","Chassis"] -> "Mod1,Mod2,Chassis"
    
    Args:
        names_in: Array of device, NVMEM area, or physical channel names
    
    Returns:
        names_out: Resulting comma-delimited list of device, NVMEM area, or
            physical channel names
    """
    _interpreter = _select_interpreter()
    return _interpreter.flatten_names(names_in)

def unflatten_names(names_in: str) -> list[str]:
    """Error a comma-delimited list or range of device, NVMEM area, or
    physical channel names into an array of names.
    
    Colon-delimited ranges will be expanded. Example: "Mod1/load0:2" ->
    ["Mod1/load0","Mod1/load1","Mod1/load2"]
    
    Comma-delimited lists will be expanded. Example: "Mod1,Mod2,Chassis" ->
    ["Mod1","Mod2","Chassis"]
    
    Args:
        names_in: Comma-delimited list of device, NVMEM area, or physical
            channel names
    
    Returns:
        names_out: Resulting array of device, NVMEM area, or physical
            channel names
    """
    _interpreter = _select_interpreter()
    return _interpreter.unflatten_names(names_in)

