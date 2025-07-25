"""SLSC Session Management Module.

This module provides the Session class for managing SLSC hardware
sessions that handle device connections, property access, command 
execution for one or more devices, physical channels, or NVMEM areas.
"""

from __future__ import annotations
from types import TracebackType

from typing_extensions import Self

from nislsc.constants import Language
from nislsc.error import SLSCError
from nislsc.library._library import Library


class Session:
    """Represent Session class for NI SLSC."""

    def __init__(self, library: Library, session_handle: int, _owns_library: bool) -> None:
        """Create a Session instance.

        Args:
            library: Previously initialized Library instance
            session_handle: The session handle returned by the
                initialization function.
        """
        self._session_handle = session_handle
        self._library = library
        self._interpreter = library._interpreter
        self._owns_library = _owns_library

    def __enter__(self) -> Self:
        """Enter the runtime context related to this object.

        Returns:
            Self: The session object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and close the Session instance.

        Args:
            type: The exception type, if an exception was raised, otherwise 
                None.
            value: The exception value, if an exception was raised, otherwise
                None.
            traceback: The traceback, if an exception was raised, otherwise 
                None.
        """
        self.close()

    def close(self) -> None:
        """Close the Session instance."""
        if self._session_handle != 0:
            self._interpreter.close_session(self._session_handle)
            self._session_handle = 0
        if self._owns_library:
            self._library.close()
            self._owns_library = False

    def get_extended_error_info(self, language: Language = Language.UNDEFINED) -> str:
        """Return extended error information for the last error that occurred on
        the specified library handle.
        
        Args:
            language: Language to return error information in
        
        Returns:
            extended_error_info: Extended error info text
        """
        language = self._library.language if language == language.UNDEFINED else language
        return self._library.get_extended_error_info(language)

    @classmethod
    def initialize_session_with_devices(cls, library: Library | None, device_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> Self:
        """Initialize an SLSC session with one or multiple devices.
        
        The session opens network connections for devices. If reservationAccess
        is set to ReadOnly or ReadWrite, the session also reserves the devices.
        
        This function saves the specified device names in the
        Session.DefaultDevices property as the default devices of the session.
        You may change the session default devices by setting the
        Session.DefaultDevices property.
        
        You cannot use the AbortSession function to cancel any blocking network
        operations performed by this function. If you need to programmatically
        abort blocking network operations, call
        InitializeSessionWithoutResources to obtain a session reference, then
        call ConnectToDevices to open network connections for the devices, and
        then call ReserveDevices to reserve the devices.
        
        Args:
            library: Previously initialized Library instance.
            device_names: Comma-delimited list of devices
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the default value.
            reservation_access: Access mode with which to reserve devices: None
                (do not reserve devices), ReadOnly, or ReadWrite
            reservation_group: Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout: Timeout for reserving devices, in seconds.
                Specify -1 to use the default value.
        
        Returns:
            Self: New instance of Session object.
        """
        try:
            owns_library = False
            if library is None:
                library = Library()
                owns_library = True
            library_handle = library._library_handle
            interpreter = library._interpreter
            session_handle = interpreter.initialize_session_with_devices(library_handle, device_names, connection_timeout, reservation_access, reservation_group, reservation_timeout)
            return cls(library, session_handle, owns_library)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def initialize_session_with_nvmem_areas(cls, library: Library | None, nvmem_area_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> Self:
        """Initialize an SLSC session with one or multiple NVMEM areas.
        
        The session opens network connections for NVMEM areas. If
        reservationAccess is set to ReadOnly or ReadWrite, the session also
        reserves the devices.
        
        This function saves the specified NVMEM area names in the
        Session.DefaultNVMEMAreas property as the default NVMEM areas of the
        session. You may change the session default NVMEM areas or session
        default devices by setting the Session.DefaultNVMEMAreas property or the
        Session.DefaultDevices property.
        
        You cannot use the AbortSession function to cancel any blocking network
        operations performed by this function. If you need to programmatically
        abort blocking network operations, call
        InitializeSessionWithoutResources to obtain a session reference, then
        call ConnectToDevices to open network connections for the devices, and
        then call ReserveDevices to reserve the devices.
        
        Args:
            library: Previously initialized Library instance.
            nvmem_area_names: Comma-delimited list of NVMEM areas
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the default value.
            reservation_access: Access mode with which to reserve devices: None
                (do not reserve devices), ReadOnly, or ReadWrite
            reservation_group: Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout: Timeout for reserving devices, in seconds.
                Specify -1 to use the default value.
        
        Returns:
            Self: New instance of Session object.
        """
        try:
            owns_library = False
            if library is None:
                library = Library()
                owns_library = True
            library_handle = library._library_handle
            interpreter = library._interpreter
            session_handle = interpreter.initialize_session_with_nvmem_areas(library_handle, nvmem_area_names, connection_timeout, reservation_access, reservation_group, reservation_timeout)
            return cls(library, session_handle, owns_library)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def initialize_session_with_physical_channels(cls, library: Library | None, physical_channel_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> Self:
        """Initialize an SLSC session with one or multiple physical channels.
        
        The session opens network connections for devices that correspond to the
        physical channels. The session opens network connections for devices
        that correspond to the physical channels. If reservationAccess is set to
        ReadOnly or ReadWrite, the session also reserves the devices.
        
        This function saves the specified physical channel names in the
        Session.DefaultPhysChans property as the default physical channels of
        the session. You may change the session default physical channels or
        session default devices by setting Session.DefaultPhysChans property or
        the Session.DefaultDevices property.
        
        You cannot use the AbortSession function to cancel any blocking network
        operations performed by this function. If you need to programmatically
        abort blocking network operations, call
        InitializeSessionWithoutResources to obtain a session reference, then
        call ConnectToDevices to open network connections for the devices, and
        then call ReserveDevices to reserve the devices.
        
        Args:
            library: Previously initialized Library instance.
            physical_channel_names: Comma-delimited list of physical channels.
                Numbered physical channels may be specified as a colon-delimited
                range, such as "Mod1/load0:3".
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the default value.
            reservation_access: Access mode with which to reserve devices: None
                (do not reserve devices), ReadOnly or ReadWrite
            reservation_group: Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout: Timeout for reserving devices, in seconds.
                Specify -1 to use the default value.
        
        Returns:
            Self: New instance of Session object.
        """
        try:
            owns_library = False
            if library is None:
                library = Library()
                owns_library = True
            library_handle = library._library_handle
            interpreter = library._interpreter
            session_handle = interpreter.initialize_session_with_physical_channels(library_handle, physical_channel_names, connection_timeout, reservation_access, reservation_group, reservation_timeout)
            return cls(library, session_handle, owns_library)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    @classmethod
    def initialize_session_without_resources(cls, library: Library | None) -> Self:
        """Initialize an SLSC session without specifying any resources or
        opening any network connections.
        
        Use InitializeSessionWithoutResources if you need to set session
        properties that control network timeouts or the ability to
        programmatically abort blocking network operations.
        
        Args:
            library: Previously initialized Library instance.
        
        Returns:
            Self: New instance of Session object.
        """
        try:
            owns_library = False
            if library is None:
                library = Library()
                owns_library = True
            library_handle = library._library_handle
            interpreter = library._interpreter
            session_handle = interpreter.initialize_session_without_resources(library_handle)
            return cls(library, session_handle, owns_library)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def abort_session(self) -> None:
        """Attempt to cancel a VI/function that blocks on network
        communications, such as ConnectToDevices() or AddNetworkChassis(),
        making it wake up and return an error.
        
        After aborting the session, the session handle/refnum remains valid, but
        VIs/functions that access network connections will return errors. To
        recover from an aborted session, close it and initialize a new one.
        
        Some operations, such as DNS lookups, cannot be aborted.
        """
        try:
            self._interpreter.abort_session(self._session_handle)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def log_in(self, chassis_name: str, username: str, password: str, connection_timeout: float, save_credentials_to_disk: bool) -> None:
        """Attempt to connect and log in to the specified SLSC chassis.
        
        If successful, the username and password are cached on the local system
        until LogOut is called. Credentials are cached across reboots.
        
        If a chassis does not have cached credentials, the SLSC driver attempts
        to use default credentials of username="anonymous" password="" when it
        opens network connections to the chassis.
        
        LogIn opens a new network connection to the chassis to test
        connectivity, and closes it afterward. LogIn does not reuse or affect
        cached network connections, nor does it cache the new network
        connection.
        
        If you set 'saveCredentialsToDisk' to true, LogIn saves the credentials
        in a platform-specific disk location and format. If cached credentials
        exist in memory, they are deleted. - Windows: SLSC stores credentials in
        your Windows Credential Manager vault. These are encrypted with your
        Windows login information. You can view/manage/delete your credentials
        via Control Panel >> User Accounts >> Credential Manager. - Pharlap ETS:
        SLSC stores credentials in a cleartext JSON file in
        c:\ni-rt\system\niwebcer\certstore\nislsc\loginCache. Each SLSC chassis
        has a separate file. Note: this path is not accessible over FTP. - NI
        Linux Real-Time: SLSC stores credentials in a cleartext JSON file in
        /home/lvuser/.config/nislsc/loginCache. Each SLSC chassis has a separate
        file.
        
        If you set 'saveCredentialsToDisk' to false, LogIn saves the credentials
        in the memory of the calling process. If cached credentials exist on
        disk, they are deleted.
        
        Args:
            chassis_name: Chassis to log in to
            username: Name of user account on the SLSC chassis
            password: Password of user account on the SLSC chassis
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the value of the Session.TCPIP.ConnectTimeout
                property.
            save_credentials_to_disk: Specify true to save login credentials to
                disk, false to keep them in memory for the lifetime of the
                process
        """
        try:
            self._interpreter.log_in(self._session_handle, chassis_name, username, password, connection_timeout, save_credentials_to_disk)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def log_out(self, chassis_name: str) -> None:
        """Delete any cached credentials for this chassis.
        
        If the specified SLSC chassis is no longer accessible but it is in the
        config file, this function still deletes the cached credentials.
        
        LogOut deletes both in-memory and on-disk credentials.
        
        Args:
            chassis_name: Chassis to log out of
        """
        try:
            self._interpreter.log_out(self._session_handle, chassis_name)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def connect_to_devices(self, device_names: str, connection_timeout: float) -> None:
        """Open network connections for the specified device(s), sharing
        connections to the same SLSC chassis.
        
        ConnectToDevices attempts to connect using all the known hostnames and
        IP addresses of the chassis until one succeeds or all have failed. If
        the connect timeout expires before a connection is successfully
        established, an error is returned. Some operations, such as DNS lookups,
        may not be abortable and may cause additional delays before a timeout
        error is returned.
        
        Args:
            device_names: Comma-delimited list of devices for which to open
                network connections. If you do not specify this parameter, the
                session default devices will be used.
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the value of the Session.TCPIP.ConnectTimeout
                property.
        """
        try:
            self._interpreter.connect_to_devices(self._session_handle, device_names, connection_timeout)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def disconnect_from_devices(self, device_names: str) -> None:
        """Close network connections for the specified devices.
        
        When multiple devices share a network connection because they are in the
        same SLSC chassis, the network connection will remain open until the
        last device is disconnected.
        
        Args:
            device_names: Comma-delimited list of devices for which to close
                network connections. If you do not specify this parameter, the
                session default devices will be used.
        """
        try:
            self._interpreter.disconnect_from_devices(self._session_handle, device_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def connect_to_chassis_by_address(self, address: str, username: str, password: str, connection_timeout: float) -> str:
        """Open a network connection for a chassis by the specified IP address
        or hostname.
        
        If the connect timeout expires before a connection is successfully
        established, an error is returned.
        
        Args:
            address: Chassis IP address or hostname
            username: Name of user account on the SLSC chassis
            password: Password of user account on the SLSC chassis
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the value of the Session.TCPIP.ConnectTimeout
                property.
        
        Returns:
            chassis_name: Name of connected chassis
        """
        try:
            chassis_name = self._interpreter.connect_to_chassis_by_address(self._session_handle, address, username, password, connection_timeout)
            return chassis_name
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def reserve_devices(self, device_names: str, reservation_access: int, reservation_group: str, reservation_timeout: float) -> None:
        """Reserve the specified device(s), which prevents other sessions from
        accessing them.
        
        You must reserve a device before using it.
        
        To reserve a device that has been reserved by another session with
        ReadWrite access, you can close the session, unreserve the device, or
        use the same reservation group name as that of the device. You can
        directly reserve a device that has been reserved by another session with
        ReadOnly access.
        
        Args:
            device_names: Comma-delimited list of devices to reserve. If you do
                not specify this parameter, the session default devices will be
                used.
            reservation_access: Access mode with which to reserve devices:
                ReadOnly or ReadWrite
            reservation_group: Arbitrary name to allow multiple sessions to
                simultaneously reserve the same device(s)
            reservation_timeout: Timeout for reserving devices, in seconds.
                Specify -1 to use the value of the Session.ReservationTimeout
                property
        """
        try:
            self._interpreter.reserve_devices(self._session_handle, device_names, reservation_access, reservation_group, reservation_timeout)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def unreserve_devices(self, device_names: str) -> None:
        """Unreserve the specified device(s), allowing other sessions to access
        them.
        
        Args:
            device_names: Comma-delimited list of devices to unreserve. If you
                do not specify this parameter, the session default devices will
                be used.
        """
        try:
            self._interpreter.unreserve_devices(self._session_handle, device_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def reset_devices(self, device_names: str) -> None:
        """Reset the specified device(s) to the default state.
        
        This function sends the specified devices a hardware reset signal,
        reinitializes module registers to their initial value, and rereads
        module non-volatile memory.
        
        If you specify a chassis, this function resets all of the modules in the
        chassis.
        
        To reboot a chassis, use the Restart function provided by the NI System
        Configuration API.
        
        Args:
            device_names: Comma-delimited list of devices to reset. If you do
                not specify this parameter, the session default devices will be
                used.
        """
        try:
            self._interpreter.reset_devices(self._session_handle, device_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def rename_device(self, device_name: str, new_device_name: str) -> None:
        """Rename the specified device, both on the remote device and in the
        local SLSC configuration file.
        
        When renaming a chassis, the hostname of the chassis will be changed on
        the chassis, but it is not updated in the configuration file. After the
        network is expected to reflect the new hostname, call AddNetworkChassis
        to update the configuration file.
        
        Args:
            device_name: Device to rename
            new_device_name: New name for device
        """
        try:
            self._interpreter.rename_device(self._session_handle, device_name, new_device_name)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def update_system_configuration_file(self, chassis_name: str, connection_timeout: float) -> None:
        """Update the information of the specified chassis and its modules in
        the local configuration file.
        
        UpdateSystemConfigFile opens a new network connection to the chassis and
        closes it afterward. UpdateSystemConfigFile does not reuse or affect
        cached network connections, nor does it cache the new network
        connection.
        
        Args:
            chassis_name: Name of chassis to update
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the value of the Session.TCPIP.ConnectTimeout
                property.
        """
        try:
            self._interpreter.update_system_configuration_file(self._session_handle, chassis_name, connection_timeout)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def add_network_chassis(self, address: str, username: str, password: str, connection_timeout: float) -> str:
        """Connect to the specified network chassis, adds the chassis and its
        modules to the system, and saves them to the local configuration file.
        
        If the chassis has already been added, calling this function again
        refreshes the modules.
        
        AddNetworkChassis opens a new network connection to the chassis and
        closes it afterward. AddNetworkChassis does not reuse or affect cached
        network connections, nor does it cache the new network connection.
        
        Args:
            address: Chassis IP address or hostname
            username: Name of user account on the SLSC chassis
            password: Password of user account on the SLSC chassis
            connection_timeout: Timeout for connecting to devices, in seconds.
                Specify -1 to use the value of the Session.TCPIP.ConnectTimeout
                property.
        
        Returns:
            chassis_name: Name of added chassis
        """
        try:
            chassis_name = self._interpreter.add_network_chassis(self._session_handle, address, username, password, connection_timeout)
            return chassis_name
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def remove_chassis(self, chassis_name: str) -> None:
        """Remove the specified chassis from the local configuration file.
        
        Note that if the chassis is still discoverable via mDNS, it will
        continue to show up in SLSC I/O controls, the Sys.Devices property, etc.
        
        Args:
            chassis_name: Name of chassis to remove
        """
        try:
            self._interpreter.remove_chassis(self._session_handle, chassis_name)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_bool(self, device_names: str, property_name: str) -> bool:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_bool(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_bool_array(self, device_names: str, property_name: str) -> list[bool]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_bool_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_double(self, device_names: str, property_name: str) -> float:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_double(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_double_array(self, device_names: str, property_name: str) -> list[float]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_double_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_int32(self, device_names: str, property_name: str) -> int:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_int32(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_int32_array(self, device_names: str, property_name: str) -> list[int]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_int32_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_int64(self, device_names: str, property_name: str) -> int:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_int64(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_int64_array(self, device_names: str, property_name: str) -> list[int]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_int64_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_string(self, device_names: str, property_name: str) -> str:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_string(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_string_array(self, device_names: str, property_name: str) -> list[str]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_string_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_uint32(self, device_names: str, property_name: str) -> int:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_uint32(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_uint32_array(self, device_names: str, property_name: str) -> list[int]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_uint32_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_uint64(self, device_names: str, property_name: str) -> int:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_uint64(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_device_property_uint64_array(self, device_names: str, property_name: str) -> list[int]:
        """Get the value of the specified device property from one or more
        devices.
        
        To get a property from multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        Args:
            device_names: Comma-delimited list of devices for which to get the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_device_property_uint64_array(self._session_handle, device_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_bool(self, device_names: str, property_name: str, property_value: bool) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_bool(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_bool_array(self, device_names: str, property_name: str, property_value: list[bool]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_bool_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_double(self, device_names: str, property_name: str, property_value: float) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_double(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_double_array(self, device_names: str, property_name: str, property_value: list[float]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_double_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_int32(self, device_names: str, property_name: str, property_value: int) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_int32(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_int32_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_int32_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_int64(self, device_names: str, property_name: str, property_value: int) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_int64(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_int64_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_int64_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_string(self, device_names: str, property_name: str, property_value: str) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_string(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_string_array(self, device_names: str, property_name: str, property_value: list[str]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_string_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_uint32(self, device_names: str, property_name: str, property_value: int) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_uint32(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_uint32_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_uint32_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_uint64(self, device_names: str, property_name: str, property_value: int) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_uint64(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_device_property_uint64_array(self, device_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified device property to a new value for one or more
        devices.
        
        To set a property for multiple devices, specify a comma-delimited list
        of devices and use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            device_names: Comma-delimited list of devices for which to set the
                specified property. If you do not specify this parameter, the
                session default devices will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_device_property_uint64_array(self._session_handle, device_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_bool(self, physical_channel_names: str, property_name: str) -> bool:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_bool(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_bool_array(self, physical_channel_names: str, property_name: str) -> list[bool]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_bool_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_double(self, physical_channel_names: str, property_name: str) -> float:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_double(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_double_array(self, physical_channel_names: str, property_name: str) -> list[float]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_double_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_int32(self, physical_channel_names: str, property_name: str) -> int:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_int32(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_int32_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_int32_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_int64(self, physical_channel_names: str, property_name: str) -> int:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_int64(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_int64_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_int64_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_string(self, physical_channel_names: str, property_name: str) -> str:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_string(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_string_array(self, physical_channel_names: str, property_name: str) -> list[str]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_string_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_uint32(self, physical_channel_names: str, property_name: str) -> int:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_uint32(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_uint32_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_uint32_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_uint64(self, physical_channel_names: str, property_name: str) -> int:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_uint64(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_physical_channel_property_uint64_array(self, physical_channel_names: str, property_name: str) -> list[int]:
        """Get the value of the specified physical channel property from one or
        more physical channels.
        
        To get a property from multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to get the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_physical_channel_property_uint64_array(self._session_handle, physical_channel_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_bool(self, physical_channel_names: str, property_name: str, property_value: bool) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_bool(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_bool_array(self, physical_channel_names: str, property_name: str, property_value: list[bool]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_bool_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_double(self, physical_channel_names: str, property_name: str, property_value: float) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_double(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_double_array(self, physical_channel_names: str, property_name: str, property_value: list[float]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_double_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_int32(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_int32(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_int32_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_int32_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_int64(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_int64(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_int64_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_int64_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_string(self, physical_channel_names: str, property_name: str, property_value: str) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_string(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_string_array(self, physical_channel_names: str, property_name: str, property_value: list[str]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_string_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_uint32(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_uint32(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_uint32_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_uint32_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_uint64(self, physical_channel_names: str, property_name: str, property_value: int) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_uint64(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_physical_channel_property_uint64_array(self, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified physical channel property to a new value for one or
        more physical channels.
        
        To set a property for multiple physical channels, specify a
        comma-delimited list or colon-delimited range of physical channels and
        use an array version of this VI/function.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s) or physical
        channels(s).
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to set the specified property. Numbered physical
                channels may be specified as a colon-delimited range, such as
                "Mod1/load0:3". If you do not specify this parameter, the
                session default physical channels will be used.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_physical_channel_property_uint64_array(self._session_handle, physical_channel_names, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_properties_for_devices(self, device_names: str) -> None:
        """Commit all device or physical channels properties with pending
        changes to hardware for the specified device(s) and the physical
        channels that they contain.
        
        If you set a property multiple times between commits, only the last
        value is committed.
        
        Args:
            device_names: Comma-delimited list of devices for which to commit
                properties. If you do not specify this parameter, the session
                default devices will be used.
        """
        try:
            self._interpreter.commit_properties_for_devices(self._session_handle, device_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_properties_for_physical_channels(self, physical_channel_names: str) -> None:
        """Commit all physical channel properties with pending changes to
        hardware for the specified physical channel(s).
        
        If you set a property multiple times between commits, only the last
        value is committed.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels
                for which to commit properties. Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                If you do not specify this parameter, the session default
                physical channels will be used.
        """
        try:
            self._interpreter.commit_properties_for_physical_channels(self._session_handle, physical_channel_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_properties_for_session(self) -> None:
        """Commit all device and physical channel properties with pending
        changes to hardware for all devices and physical channels used by the
        session.
        
        If you set a property multiple times between commits, only the last
        value is committed.
        """
        try:
            self._interpreter.commit_properties_for_session(self._session_handle)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_properties_generic(self, resources: str) -> None:
        """Commit all properties with pending changes to hardware for the
        specified resource(s).
        
        If you set a property multiple times between commits, only the last
        value is committed.
        
        Args:
            resources: Comma-delimited list of resources for which to commit
                properties, or a resource alias such as "$DefaultDevices".
                Numbered physical channels may be specified as a colon-delimited
                range, such as "Mod1/load0:3". This parameter is required.
        """
        try:
            self._interpreter.commit_properties_generic(self._session_handle, resources)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_area_property_bool(self, nvmem_area_names: str, property_name: str) -> bool:
        """Get the value of the specified NVMEM area property for one or more
        NVMEM areas.
        
        To get a property from multiple NVMEM areas, specify a comma-delimited
        list of NVMEM areas and use an array version of this VI/function.
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas for which to
                get the specified property. Specify "Default" to use the value
                of the Session.DefaultNVMEMAreas property.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_nvmem_area_property_bool(self._session_handle, nvmem_area_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_area_property_bool_array(self, nvmem_area_names: str, property_name: str) -> list[bool]:
        """Get the value of the specified NVMEM area property for one or more
        NVMEM areas.
        
        To get a property from multiple NVMEM areas, specify a comma-delimited
        list of NVMEM areas and use an array version of this VI/function.
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas for which to
                get the specified property. Specify "Default" to use the value
                of the Session.DefaultNVMEMAreas property.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_nvmem_area_property_bool_array(self._session_handle, nvmem_area_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_area_property_string(self, nvmem_area_names: str, property_name: str) -> str:
        """Get the value of the specified NVMEM area property for one or more
        NVMEM areas.
        
        To get a property from multiple NVMEM areas, specify a comma-delimited
        list of NVMEM areas and use an array version of this VI/function.
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas for which to
                get the specified property. Specify "Default" to use the value
                of the Session.DefaultNVMEMAreas property.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_nvmem_area_property_string(self._session_handle, nvmem_area_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_area_property_string_array(self, nvmem_area_names: str, property_name: str) -> list[str]:
        """Get the value of the specified NVMEM area property for one or more
        NVMEM areas.
        
        To get a property from multiple NVMEM areas, specify a comma-delimited
        list of NVMEM areas and use an array version of this VI/function.
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas for which to
                get the specified property. Specify "Default" to use the value
                of the Session.DefaultNVMEMAreas property.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_nvmem_area_property_string_array(self._session_handle, nvmem_area_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_area_property_uint32(self, nvmem_area_names: str, property_name: str) -> int:
        """Get the value of the specified NVMEM area property for one or more
        NVMEM areas.
        
        To get a property from multiple NVMEM areas, specify a comma-delimited
        list of NVMEM areas and use an array version of this VI/function.
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas for which to
                get the specified property. Specify "Default" to use the value
                of the Session.DefaultNVMEMAreas property.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_nvmem_area_property_uint32(self._session_handle, nvmem_area_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_area_property_uint32_array(self, nvmem_area_names: str, property_name: str) -> list[int]:
        """Get the value of the specified NVMEM area property for one or more
        NVMEM areas.
        
        To get a property from multiple NVMEM areas, specify a comma-delimited
        list of NVMEM areas and use an array version of this VI/function.
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas for which to
                get the specified property. Specify "Default" to use the value
                of the Session.DefaultNVMEMAreas property.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_nvmem_area_property_uint32_array(self._session_handle, nvmem_area_names, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_session_property_double(self, property_name: str) -> float:
        """Get the value of the specified session property.
        
        Args:
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_session_property_double(self._session_handle, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_session_property_string(self, property_name: str) -> str:
        """Get the value of the specified session property.
        
        Args:
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_session_property_string(self._session_handle, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_session_property_string_array(self, property_name: str) -> list[str]:
        """Get the value of the specified session property.
        
        Args:
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_session_property_string_array(self._session_handle, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_session_property_double(self, property_name: str, property_value: float) -> None:
        """Set the specified session property to a new value.
        
        The change takes effect immediately.
        
        Args:
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_session_property_double(self._session_handle, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_session_property_string(self, property_name: str, property_value: str) -> None:
        """Set the specified session property to a new value.
        
        The change takes effect immediately.
        
        Args:
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_session_property_string(self._session_handle, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_session_property_string_array(self, property_name: str, property_value: list[str]) -> None:
        """Set the specified session property to a new value.
        
        The change takes effect immediately.
        
        Args:
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_session_property_string_array(self._session_handle, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_system_property_double(self, property_name: str) -> float:
        """Get the value of the specified system property.
        
        Args:
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_system_property_double(self._session_handle, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_system_property_string_array(self, property_name: str) -> list[str]:
        """Get the value of the specified system property.
        
        Args:
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_system_property_string_array(self._session_handle, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_system_property_uint64(self, property_name: str) -> int:
        """Get the value of the specified system property.
        
        Args:
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_system_property_uint64(self._session_handle, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_system_property_double(self, property_name: str, property_value: float) -> None:
        """Set the specified system property to a new value.
        
        The change takes effect immediately.
        
        Args:
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_system_property_double(self._session_handle, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_bool(self, resources: str, property_name: str) -> bool:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_bool(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_bool_array(self, resources: str, property_name: str) -> list[bool]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_bool_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_double(self, resources: str, property_name: str) -> float:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_double(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_double_array(self, resources: str, property_name: str) -> list[float]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_double_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_int32(self, resources: str, property_name: str) -> int:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_int32(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_int32_array(self, resources: str, property_name: str) -> list[int]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_int32_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_int64(self, resources: str, property_name: str) -> int:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_int64(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_int64_array(self, resources: str, property_name: str) -> list[int]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_int64_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_string(self, resources: str, property_name: str) -> str:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_string(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_string_array(self, resources: str, property_name: str) -> list[str]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_string_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_uint32(self, resources: str, property_name: str) -> int:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_uint32(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_uint32_array(self, resources: str, property_name: str) -> list[int]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_uint32_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_uint64(self, resources: str, property_name: str) -> int:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_uint64(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_generic_property_uint64_array(self, resources: str, property_name: str) -> list[int]:
        """Get the value of the specified property from one or more resources,
        the session, or the system.
        
        To get a property from multiple resources, specify a comma-delimited
        list of resources and use an array version of this VI/function.
        
        Args:
            resources: Comma-delimited list of resources for which to get the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to get
        
        Returns:
            property_value: Value of property
        """
        try:
            property_value = self._interpreter.get_generic_property_uint64_array(self._session_handle, resources, property_name)
            return property_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_bool(self, resources: str, property_name: str, property_value: bool) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_bool(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_bool_array(self, resources: str, property_name: str, property_value: list[bool]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_bool_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_double(self, resources: str, property_name: str, property_value: float) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_double(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_double_array(self, resources: str, property_name: str, property_value: list[float]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_double_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_int32(self, resources: str, property_name: str, property_value: int) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_int32(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_int32_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_int32_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_int64(self, resources: str, property_name: str, property_value: int) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_int64(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_int64_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_int64_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_string(self, resources: str, property_name: str, property_value: str) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_string(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_string_array(self, resources: str, property_name: str, property_value: list[str]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_string_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_uint32(self, resources: str, property_name: str, property_value: int) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_uint32(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_uint32_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_uint32_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_uint64(self, resources: str, property_name: str, property_value: int) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_uint64(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_generic_property_uint64_array(self, resources: str, property_name: str, property_value: list[int]) -> None:
        """Set the specified property to a new value for one or more resources,
        the session, or the system.
        
        If the property is defined by the SLSC driver, the change takes effect
        immediately. If the property is defined by the device(s), the change
        takes effect when properties are committed for the device(s).
        
        Args:
            resources: Comma-delimited list of resources for which to set the
                specified property, or a resource alias such as
                "$DefaultDevices" or "$System". Numbered physical channels may
                be specified as a colon-delimited range, such as "Mod1/load0:3".
                This parameter is required.
            property_name: Name of property to set
            property_value: New value to set property to
        """
        try:
            self._interpreter.set_generic_property_uint64_array(self._session_handle, resources, property_name, property_value)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def execute_device_command(self, device_names: str, command_name: str, timeout: float) -> None:
        """Execute the specified device command on one or more devices.
        
        Commands define how user applications initiate actions or coordinated
        state changes on the SLSC module. For example, user applications may
        execute a command to reset a switch scanlist or append a new entry to
        it. Commands have no explicit parameters, but they may latch or modify
        the values of properties, registers, and bitfields.
        
        If any properties in this context have pending changes, they are
        committed before the command is executed.
        
        Each command is identified by name and may be supported on a per-module
        or per-physical-channel basis.
        
        Args:
            device_names: Comma-delimited list of devices on which to execute
                the command. If you do not specify this parameter, the session
                default devices will be used.
            command_name: Name of command to execute
            timeout: Timeout in seconds
        """
        try:
            self._interpreter.execute_device_command(self._session_handle, device_names, command_name, timeout)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def execute_physical_channel_command(self, physical_channel_names: str, command_name: str, timeout: float) -> None:
        """Execute the specified physical channel command on one or more
        physical channels.
        
        Commands define how user applications initiate actions or coordinated
        state changes on the SLSC module. For example, user applications may
        execute a command to reset a switch scanlist or append a new entry to
        it. Commands have no explicit parameters, but they may latch or modify
        the values of properties, registers, and bitfields.
        
        If any properties in this context have pending changes, they are
        committed before the command is executed.
        
        Each command is identified by name and may be supported on a per-module
        or per-physical-channel basis.
        
        Args:
            physical_channel_names: Comma-delimited list of physical channels on
                which to execute the command. If you do not specify this
                parameter, the session default physical channels will be used.
            command_name: Name of command to execute
            timeout: Timeout in seconds
        """
        try:
            self._interpreter.execute_physical_channel_command(self._session_handle, physical_channel_names, command_name, timeout)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def execute_generic_command(self, resources: str, command_name: str, timeout: float) -> None:
        """Execute the specified command on one or more resources.
        
        Commands define how user applications initiate actions or coordinated
        state changes on the SLSC module. For example, user applications may
        execute a command to reset a switch scanlist or append a new entry to
        it. Commands have no explicit parameters, but they may latch or modify
        the values of properties, registers, and bitfields.
        
        If any properties in this context have pending changes, they are
        committed before the command is executed.
        
        Each command is identified by name and may be supported on a per-module
        or per-physical-channel basis.
        
        Args:
            resources: Comma-delimited list of resources for which to execute
                the command, or a resource alias such as "$DefaultDevices".
                Numbered physical channels may be specified as a colon-delimited
                range, such as "Mod1/load0:3". This parameter is required.
            command_name: Name of command to execute
            timeout: Timeout in seconds
        """
        try:
            self._interpreter.execute_generic_command(self._session_handle, resources, command_name, timeout)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def read_register_uint8(self, device_name: str, register_address: int) -> int:
        """Read the specified register.
        
        To read a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
        
        Returns:
            data: Register data
        """
        try:
            data = self._interpreter.read_register_uint8(self._session_handle, device_name, register_address)
            return data
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def read_register_uint16(self, device_name: str, register_address: int) -> int:
        """Read the specified register.
        
        To read a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
        
        Returns:
            data: Register data
        """
        try:
            data = self._interpreter.read_register_uint16(self._session_handle, device_name, register_address)
            return data
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def read_register_uint32(self, device_name: str, register_address: int) -> int:
        """Read the specified register.
        
        To read a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
        
        Returns:
            data: Register data
        """
        try:
            data = self._interpreter.read_register_uint32(self._session_handle, device_name, register_address)
            return data
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def read_register_uint64(self, device_name: str, register_address: int) -> int:
        """Read the specified register.
        
        To read a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
        
        Returns:
            data: Register data
        """
        try:
            data = self._interpreter.read_register_uint64(self._session_handle, device_name, register_address)
            return data
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def write_register_uint8(self, device_name: str, register_address: int, data: int) -> None:
        """Write data to the specified register.
        
        To write a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
            data: New register data
        """
        try:
            self._interpreter.write_register_uint8(self._session_handle, device_name, register_address, data)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def write_register_uint16(self, device_name: str, register_address: int, data: int) -> None:
        """Write data to the specified register.
        
        To write a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
            data: New register data
        """
        try:
            self._interpreter.write_register_uint16(self._session_handle, device_name, register_address, data)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def write_register_uint32(self, device_name: str, register_address: int, data: int) -> None:
        """Write data to the specified register.
        
        To write a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
            data: New register data
        """
        try:
            self._interpreter.write_register_uint32(self._session_handle, device_name, register_address, data)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def write_register_uint64(self, device_name: str, register_address: int, data: int) -> None:
        """Write data to the specified register.
        
        To write a single bitfield, consider using properties instead.
        
        Args:
            device_name: Name of module. If you do not specify this parameter,
                the session default devices will be used. If you specify more
                than one device (either explicitly or by leaving this parameter
                unspecified when the session has more than one default device),
                an error will be returned.
            register_address: Address of register
            data: New register data
        """
        try:
            self._interpreter.write_register_uint64(self._session_handle, device_name, register_address, data)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_nvmem_bytes(self, nvmem_area: str, nvmem_address: int, num_byte: int) -> bytes:
        """Get a range of bytes from an NVMEM area.
        
        Args:
            nvmem_area: NVMEM area from which to get data. If you do not specify
                this parameter, the session default NVMEM areas will be used.
            nvmem_address: Address of NVMEM area
        
        Returns:
            byte: NVMEM data
        """
        try:
            byte = self._interpreter.get_nvmem_bytes(self._session_handle, nvmem_area, nvmem_address, num_byte)
            return byte
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_nvmem_bytes(self, nvmem_area: str, nvmem_address: int, bytes_data: bytes, serial_number: str, password: str) -> None:
        """Set a range of bytes to write to an NVMEM area.
        
        The data is cached in the session until the NVMEM area is committed. If
        you close the session without committing the NVMEM areas, the cached
        data is discarded.
        
        Some areas in the NVMEM of an SLSC module may be protected. You need to
        specify a serial number and password to write to protected areas.
        
        Args:
            nvmem_area: NVMEM area for which to set data. If you do not specify
                this parameter, the session default NVMEM areas will be used.
            nvmem_address: Address of data within NVMEM area
            byte: New NVMEM data
            serial_number: Serial number of the hardware. Do not specify this
                parameter if the NVMEM area is not protected.
            password: Password of the NVMEM area. Do not specify this parameter
                if the NVMEM area is not protected.
        """
        try:
            self._interpreter.set_nvmem_bytes(self._session_handle, nvmem_area, nvmem_address, bytes_data, serial_number, password)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_nvmem_areas(self, nvmem_area_names: str) -> None:
        """Commit pending changes to hardware for the specified NVMEM area(s).
        
        Args:
            nvmem_area_names: Comma-delimited list of NVMEM areas to commit. If
                you do not specify this parameter, the session default NVMEM
                areas will be used.
        """
        try:
            self._interpreter.commit_nvmem_areas(self._session_handle, nvmem_area_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_nvmem_for_devices(self, device_names: str) -> None:
        """Commit pending changes to hardware for all NVMEM areas on the
        specified device(s).
        
        Args:
            device_names: Comma-delimited list of devices to commit. If you do
                not specify this parameter, the session default devices will be
                used.
        """
        try:
            self._interpreter.commit_nvmem_for_devices(self._session_handle, device_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_nvmem_for_session(self) -> None:
        """Commit pending changes to hardware for all NVMEM areas for all
        modules in the session.
        
        If the session has any chassis reserved, this VI/function skips over
        them.
        """
        try:
            self._interpreter.commit_nvmem_for_session(self._session_handle)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_nvmem_generic(self, resources: str) -> None:
        """Commit pending changes to hardware for the specified resource(s).
        
        Args:
            resources: Comma-delimited list of resources for which to commit
                NVMEM, or a resource alias such as "$DefaultDevices". This
                parameter is required.
        """
        try:
            self._interpreter.commit_nvmem_generic(self._session_handle, resources)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_linear_scaling_parameters(self, physical_channel_names: str) -> tuple[float, float]:
        """Get scaling parameters from a linear scale that uses the equation y =
        mx + b, where x is a pre-scaled value and y is a scaled value.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
        
        Returns:
            slope: Slope value to get.
            intercept: Intercept value to get.
        """
        try:
            intercept = self._interpreter.get_linear_scaling_parameters(self._session_handle, physical_channel_names)
            return intercept
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_polynomial_scaling_parameters(self, physical_channel_names: str) -> tuple[list[float], list[float]]:
        """Get scaling parameters from a polynomial scale that uses an nth order
        polynomial equation.
        
        A polynomial scale contains both a polynomial to convert pre-scaled
        values to scaled values and a polynomial to convert scaled values to
        pre-scaled values.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
        
        Returns:
            forward_coefficient: Forward coefficients to get.
            reverse_coefficient: Reverse coefficients to get.
        """
        try:
            reverse_coefficient = self._interpreter.get_polynomial_scaling_parameters(self._session_handle, physical_channel_names)
            return reverse_coefficient
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_table_scaling_parameters(self, physical_channel_names: str) -> tuple[list[float], list[float], int]:
        """Get scaling parameters from a table scale that maps an array of
        pre-scaled values to an array of corresponding scaled values.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
        
        Returns:
            scaled_value: Scaled Values to get.
            prescale_value: Prescale Values to get.
            coercion: Coercion to get.
        """
        try:
            coercion = self._interpreter.get_table_scaling_parameters(self._session_handle, physical_channel_names)
            return coercion
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_user_defined_scaling_parameters(self, physical_channel_names: str) -> tuple[list[str], list[float]]:
        """Get scaling parameters from a user-defined scale.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
        
        Returns:
            user_defined_parameter_names: User-defined parameter names to get.
            user_defined_parameter_value: User-defined parameters to get.
        """
        try:
            user_defined_parameter_value = self._interpreter.get_user_defined_scaling_parameters(self._session_handle, physical_channel_names)
            return user_defined_parameter_value
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def get_user_defined_scaling_equation(self, physical_channel_names: str) -> str:
        """Get a scaling equation from a user-defined scale.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
        
        Returns:
            user_defined_equation: User-defined equation to get.
        """
        try:
            user_defined_equation = self._interpreter.get_user_defined_scaling_equation(self._session_handle, physical_channel_names)
            return user_defined_equation
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_linear_scaling_parameters(self, physical_channel_names: str, slope: float, intercept: float, serial_number: str, password: str) -> None:
        """Set scaling parameters for a linear scale that uses the equation y =
        mx + b, where x is a pre-scaled value and y is a scaled value.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
            slope: Slope value to set.
            intercept: Intercept value to set.
            serial_number: Serial number of the hardware. You do not have to
                specify this parameter if the NVMEM area is not protected.
            password: Password of the scaling area. You do not have to specify
                this parameter if the scaling area is not protected.
        """
        try:
            self._interpreter.set_linear_scaling_parameters(self._session_handle, physical_channel_names, slope, intercept, serial_number, password)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_polynomial_scaling_parameters(self, physical_channel_names: str, forward_coefficient: list[float], reverse_coefficient: list[float], serial_number: str, password: str) -> None:
        """Set scaling parameters for a polynomial scale that uses an nth order
        polynomial equation.
        
        A polynomial scale contains both a polynomial to convert pre-scaled
        values to scaled values and a polynomial to convert scaled values to
        pre-scaled values.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
            forward_coefficient: Forward coefficients to set.
            reverse_coefficient: Reverse coefficients to set.
            serial_number: Serial number of the hardware. You do not have to
                specify this parameter if the NVMEM area is not protected.
            password: Password of the scaling area. You do not have to specify
                this parameter if the scaling area is not protected.
        """
        try:
            self._interpreter.set_polynomial_scaling_parameters(self._session_handle, physical_channel_names, forward_coefficient, reverse_coefficient, serial_number, password)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_table_scaling_parameters(self, physical_channel_names: str, scaled_value: list[float], prescale_value: list[float], coercion: int, serial_number: str, password: str) -> None:
        """Set scaling parameters for a table scale that maps an array of
        pre-scaled values to an array of corresponding scaled values.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
            scaled_value: Scaled Values to set.
            prescale_value: Prescale Values to set.
            coercion: Coercion to set.
            serial_number: Serial number of the hardware. You do not have to
                specify this parameter if the NVMEM area is not protected.
            password: Password of the scaling area. You do not have to specify
                this parameter if the scaling area is not protected.
        """
        try:
            self._interpreter.set_table_scaling_parameters(self._session_handle, physical_channel_names, scaled_value, prescale_value, coercion, serial_number, password)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_user_defined_scaling_parameters(self, physical_channel_names: str, user_defined_parameter_name: list[str], user_defined_parameter_value: list[float], serial_number: str, password: str) -> None:
        """Set scaling parameters for a user-defined scale.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
            user_defined_parameter_name: parameter names
            user_defined_parameter_value: User-defined parameters to set.
            serial_number: Serial number of the hardware. You do not have to
                specify this parameter if the NVMEM area is not protected.
            password: Password of the scaling area. You do not have to specify
                this parameter if the scaling area is not protected.
        """
        try:
            self._interpreter.set_user_defined_scaling_parameters(self._session_handle, physical_channel_names, user_defined_parameter_name, user_defined_parameter_value, serial_number, password)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def set_user_defined_scaling_equation(self, physical_channel_names: str, user_defined_equation: str, serial_number: str, password: str) -> None:
        """Set the scaling equation for a user-defined scale.
        
        Args:
            physical_channel_names: Physical channel where the Scaling is
                located, or a resource alias such as "$DefaultPhysChans".
            user_defined_equation: user-defined equation to set.
            serial_number: Serial number of the hardware. You do not have to
                specify this parameter if the NVMEM area is not protected.
            password: Password of the scaling area. You do not have to specify
                this parameter if the scaling area is not protected.
        """
        try:
            self._interpreter.set_user_defined_scaling_equation(self._session_handle, physical_channel_names, user_defined_equation, serial_number, password)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

    def commit_scaling_for_devices(self, device_names: str) -> None:
        """Commit all scaling parameters with pending changes to all physical
        channels that the devices contain.
        
        Args:
            device_names: Comma-delimited list of devices for which to commit
                the scaling changes.
        """
        try:
            self._interpreter.commit_scaling_for_devices(self._session_handle, device_names)
        except SLSCError as e:
            extended_info = self.get_extended_error_info()
            raise SLSCError(extended_info, e.error_code) from None

