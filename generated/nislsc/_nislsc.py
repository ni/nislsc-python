from nislsc._library_interpreter import LibraryInterpreter
from nislsc.library._library import Library
from nislsc.constants import Language
from types import TracebackType

class NISLSC():
    """Represents the NI SLSC interface.

    This class provides methods to initialize the SLSC library and access its functions.
    It manages the library interpreter and provides a context manager for resource cleanup.
    """
    def __init__(self) -> None:
        """Initializes the SLSC interface."""
        self._interpreter = LibraryInterpreter()

    def __enter__(self) -> "NISLSC":
        """Enter the runtime context related to this object."""
        return self
        
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context."""
        pass

    def initialize_library(self, version: int = 0, language: Language = Language.CURRENT_THREAD_LOCALE) -> Library:
        """Initializes the SLSC library.

        Args:
            version (int): The version of the library to initialize.
            language (Language): The language to use for error messages and outputs.

        Returns:
            int: The library handle.
        """
        return Library(self._interpreter.initialize_library(version or self._interpreter.get_library_version()), self._interpreter, language)

    def flatten_names(self, names_in: list[str]) -> str:
        """Converts an array of device, NVMEM area, or physical channel names into a comma-delimited list of names.
        
        If the array contains physical channel-style names with consecutive
            numeric suffixes, they will be collapsed into a colon-delimited
            range. Example: ["Mod1/load0","Mod1/load1","Mod1/load2"] ->
            "Mod1/load0:2"
        
        All other names will be collapsed into comma-delimited lists. Example:
            ["Mod1","Mod2","Chassis"] -> "Mod1,Mod2,Chassis"
        
        Args:
            names_in (list[str]): Array of device, NVMEM area, or physical channel
                names
        
        Returns:
            names_out (str): Resulting comma-delimited list of device, NVMEM area,
                or physical channel names
        """
        return self._interpreter.flatten_names(names_in)

    def unflatten_names(self, names_in: str) -> list[str]:
        """Converts a comma-delimited list or range of device, NVMEM area, or physical channel names into an array of names.
        
        Colon-delimited ranges will be expanded. Example: "Mod1/load0:2" ->
            ["Mod1/load0","Mod1/load1","Mod1/load2"]
        
        Comma-delimited lists will be expanded. Example: "Mod1,Mod2,Chassis" ->
            ["Mod1","Mod2","Chassis"]
        
        Args:
            names_in (str): Comma-delimited list of device, NVMEM area, or physical
                channel names
        
        Returns:
            names_out (list[str]): Resulting array of device, NVMEM area, or
                physical channel names
        """
        return self._interpreter.unflatten_names(names_in)

