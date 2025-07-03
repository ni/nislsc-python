from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language
from nislsc.session._session import Session
from types import TracebackType

class Library():
    """Represents the NI SLSC Library interface.

    This class manages the library handle and interpreter, and provides methods
    for session initialization, error handling, and resource management.
    """
    def __init__(self, interpreter: BaseInterpreter, version: int = 0, language: Language = Language.CURRENT_THREAD_LOCALE) -> None:
        """Initializes a Library instance.

        Args:
            interpreter (LibraryInterpreter): The interpreter for the SLSC library.
            version (int): The version of the library to initialize.
            language (Language): The language to use for error messages and outputs.
        """
        self._interpreter = interpreter
        self._library_handle = self._interpreter.initialize_library(version or self._interpreter.get_library_version())
        self._language = language

    def __enter__(self) -> "Library":
        """Enter the runtime context related to this object.

        Returns:
            Library: The library object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and finalize the library handle.

        Args:
            type (type[BaseException] | None): The exception type, if an exception was raised, otherwise None.
            value (BaseException | None): The exception value, if an exception was raised, otherwise None.
            traceback (TracebackType | None): The traceback, if an exception was raised, otherwise None.
        """
        self._interpreter.finalize_library(self._library_handle)
        self._library_handle = 0

    def __del__(self) -> None:
        """Destructor to ensure the library is finalized when the object is deleted."""
        if self._library_handle != 0:
            self._interpreter.finalize_library(self._library_handle)

    @property
    def language(self) -> Language:
        """Gets the current language setting.

        Returns:
            Language: An enum representing the current language.
        """
        return self._language

    @language.setter
    def language(self, language: Language) -> None:
        """Sets the language for error messages and other outputs.

        Args:
            language (Language): The language to set.
        """
        self._language = language

    def get_extended_error_info(self, language: Language = Language.UNDEFINED) -> str:
        """Returns extended error information for the last error that occurred on the specified library handle.
        
        Args:
            language (int): Language to return error information in
        
        Returns:
            extended_error_info (str): Extended error info text
        """
        language = self._language if language == Language.UNDEFINED else language
        return self._interpreter.get_extended_error_info(self._library_handle, language)

    def get_error_description(self, status_code: int, language: Language = Language.UNDEFINED) -> str:
        """Returns the error description for the specified status code.
        
        Args:
            status_code (int): Status code to look up
            language (int): Language to return error information in
        
        Returns:
            error_description (str): Error description text
        """
        language = self._language if language == Language.UNDEFINED else language
        return self._interpreter.get_error_description(self._library_handle, status_code, language)

    def initialize_session_with_devices(self, device_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> Session:
        """Initializes an SLSC session with one or multiple devices. The session opens network connections for devices. If reservationAccess is set to ReadOnly or ReadWrite, the session also reserves the devices.
        
        This function saves the specified device names in the
            Session.DefaultDevices property as the default devices of the
            session. You may change the session default devices by setting the
            Session.DefaultDevices property.
        
        You cannot use the AbortSession function to cancel any blocking network
            operations performed by this function. If you need to
            programmatically abort blocking network operations, call
            InitializeSessionWithoutResources to obtain a session reference,
            then call ConnectToDevices to open network connections for the
            devices, and then call ReserveDevices to reserve the devices.
        
        Args:
            device_names (str): Comma-delimited list of devices
            connection_timeout (float): Timeout for connecting to devices, in
                seconds. Specify -1 to use the default value.
            reservation_access (int): Access mode with which to reserve devices:
                None (do not reserve devices), ReadOnly, or ReadWrite
            reservation_group (str): Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout (float): Timeout for reserving devices, in seconds.
                Specify -1 to use the default value.
        
        Returns:
            Session: An instance of the Session class.
        """
        return Session(self._interpreter.initialize_session_with_devices(self._library_handle, device_names, connection_timeout, reservation_access, reservation_group, reservation_timeout), self._interpreter)

    def initialize_session_with_nvmem_areas(self, nvmem_area_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> Session:
        """Initializes an SLSC session with one or multiple NVMEM areas. The session opens network connections for NVMEM areas. If reservationAccess is set to ReadOnly or ReadWrite, the session also reserves the devices.
        
        This function saves the specified NVMEM area names in the
            Session.DefaultNVMEMAreas property as the default NVMEM areas of
            the session. You may change the session default NVMEM areas or
            session default devices by setting the Session.DefaultNVMEMAreas
            property or the Session.DefaultDevices property.
        
        You cannot use the AbortSession function to cancel any blocking network
            operations performed by this function. If you need to
            programmatically abort blocking network operations, call
            InitializeSessionWithoutResources to obtain a session reference,
            then call ConnectToDevices to open network connections for the
            devices, and then call ReserveDevices to reserve the devices.
        
        Args:
            nvmem_area_names (str): Comma-delimited list of NVMEM areas
            connection_timeout (float): Timeout for connecting to devices, in
                seconds. Specify -1 to use the default value.
            reservation_access (int): Access mode with which to reserve devices:
                None (do not reserve devices), ReadOnly, or ReadWrite
            reservation_group (str): Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout (float): Timeout for reserving devices, in seconds.
                Specify -1 to use the default value.
        
        Returns:
            Session: An instance of the Session class.
        """
        return Session(self._interpreter.initialize_session_with_nvmem_areas(self._library_handle, nvmem_area_names, connection_timeout, reservation_access, reservation_group, reservation_timeout), self._interpreter)

    def initialize_session_with_physical_channels(self, physical_channel_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> Session:
        """Initializes an SLSC session with one or multiple physical channels. The session opens network connections for devices that correspond to the physical channels. The session opens network connections for devices that correspond to the physical channels. If reservationAccess is set to ReadOnly or ReadWrite, the session also reserves the devices.
        
        This function saves the specified physical channel names in the
            Session.DefaultPhysChans property as the default physical channels
            of the session. You may change the session default physical
            channels or session default devices by setting
            Session.DefaultPhysChans property or the Session.DefaultDevices
            property.
        
        nYou cannot use the AbortSession function to cancel any blocking
            network operations performed by this function. If you need to
            programmatically abort blocking network operations, call
            InitializeSessionWithoutResources to obtain a session reference,
            then call ConnectToDevices to open network connections for the
            devices, and then call ReserveDevices to reserve the devices.
        
        Args:
            physical_channel_names (str): Comma-delimited list of physical
                channels. Numbered physical channels may be specified as a
                colon-delimited range, such as "Mod1/load0:3".
            connection_timeout (float): Timeout for connecting to devices, in
                seconds. Specify -1 to use the default value.
            reservation_access (int): Access mode with which to reserve devices:
                None (do not reserve devices), ReadOnly or ReadWrite
            reservation_group (str): Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout (float): Timeout for reserving devices, in seconds.
                Specify -1 to use the default value.
        
        Returns:
            Session: An instance of the Session class.
        """
        return Session(self._interpreter.initialize_session_with_physical_channels(self._library_handle, physical_channel_names, connection_timeout, reservation_access, reservation_group, reservation_timeout), self._interpreter)

    def initialize_session_without_resources(self) -> Session:
        """Initializes an SLSC session without specifying any resources or opening any network connections.
        
        Use InitializeSessionWithoutResources if you need to set session
            properties that control network timeouts or the ability to
            programmatically abort blocking network operations.
        
        Returns:
            Session: An instance of the Session class.
        """
        return Session(self._interpreter.initialize_session_without_resources(self._library_handle), self._interpreter)

