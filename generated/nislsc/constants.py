"""Define SLSC constants and enumerations.

This module provides enumeration classes that define constants and
configuration values used throughout the SLSC API.
"""

from enum import Enum
from typing import TYPE_CHECKING

try:
    from enum import StrEnum  # Python 3.11+
except ImportError:
    if not TYPE_CHECKING:

        class StrEnum(str, Enum):
            """StrEnum fallback for Python versions < 3.11."""


class ReservationAccess(Enum):
    """Define SLSC reservation access modes."""

    NONE = 0
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = 3


class PropertyAccess(Enum):
    """Define SLSC property access permissions."""

    NONE = 0
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = 3


class DataType(Enum):
    """Specify SLSC data types and array variants."""

    NONE = 0
    BOOL = 1
    DOUBLE = 2
    INT32 = 3
    INT64 = 4
    STRING = 5
    UINT32 = 6
    UINT64 = 7
    BOOL_ARRAY = 8
    DOUBLE_ARRAY = 9
    INT32_ARRAY = 10
    INT64_ARRAY = 11
    STRING_ARRAY = 12
    UINT32_ARRAY = 13
    UINT64_ARRAY = 14


class TableScaleCoercion(Enum):
    """Control table scaling coercion behavior."""

    INTERPOLATE = 0
    ROUND_TO_NEAREST = 1
    STRICT = 2


class Language(Enum):
    """Specify language codes for localized messages."""

    UNDEFINED = -1
    CURRENT_THREAD_LOCALE = 0
    ENGLISH = 1033
    FRENCH = 1036
    GERMAN = 1031
    JAPANESE = 1041
    KOREAN = 1042
    SIMPLIFIED_CHINESE = 2052


class ProductCategory(Enum):
    """Identify SLSC product categories."""

    UNKNOWN = 0
    SLSC_CHASSIS = 1
    SLSC_MODULE = 2


class CommandProperty(StrEnum):
    """Define SLSC Command properties."""

    DESCRIPTION = "Cmd.Descr"
    """Indicates a concise description of the command, as a sentence fragment. This can be used to populate UI elements."""
    DOCUMENTATION = "Cmd.Doc"
    """Indicates optional documentation for the command."""


class DeviceProperty(StrEnum):
    """Define SLSC Device properties."""

    CAPABILITIES_VERSION = "Dev.CapsVersion"
    """Indicates the capabilities verion of the module."""
    CHASSIS = "Dev.Chassis"
    """Indicates the name of the chassis that contains this module."""
    COMMANDS = "Dev.Commands"
    """Indicates the names of device commands defined by the device."""
    DESCRIPTION = "Dev.Descr"
    """Indicates a concise description of the device, as a sentence fragment. This can be used to populate UI elements."""
    HARDWARE_VERSION = "Dev.HardwareVersion"
    """Indicates the hardware version of the device."""
    MODULES = "Dev.Modules"
    """Indicates the names of the modules in the chassis."""
    NUMBER_OF_SLOTS = "Dev.NumSlots"
    """Indicates the number of total slots available for the chassis."""
    ADDED_TO_LOCAL_CONFIGURATION = "Dev.AddedToLocalConfig"
    """Indicates whether the device is added to the local configuration file."""
    CAPABILITIES_JSON = "Dev.CapsJSON"
    """Indicates the capabilities JSON content of the device."""
    NVMEM_AREAS = "Dev.NVMEM.Areas"
    """Indicates the names of the NVMEM areas available on the device."""
    NVMEM_SIZE = "Dev.NVMEM.Size"
    """Indicates the total size of the NVMEM on the device, in bytes."""
    NVMEM_BLOCK_SIZE = "Dev.NVMEM.BlockSize"
    """Indicates the block size of the NVMEM on the device, in bytes."""
    PHYSICAL_CHANNELS = "Dev.PhysChans"
    """Indicates the names of the physical channels available on the device."""
    PRODUCT_CATEGORY = "Dev.ProductCategory"
    """Indicates the product category of the device."""
    PRODUCT_NUMBER = "Dev.ProductNum"
    """Indicates the vendor-assigned unique hardware identification number for the device. Multiple vendors may assign their devices the same product number, so both Dev.VendorNum and Dev.ProductNum are required to uniquely identify a device model/type."""
    PRODUCT_NAME = "Dev.ProductName"
    """Indicates the product/model name of the device."""
    PROPERTIES = "Dev.Properties"
    """Indicates the names of device properties defined by the device. Also see Sys.DeviceProperties for driver-defined device properties."""
    SERIAL_NUMBER = "Dev.SerialNum"
    """Indicates the serial number of the device. Multiple vendors may assign their devices the same serial number, so Dev.VendorNum, Dev.ProductNum, and Dev.SerialNum are required to uniquely identify a device instance."""
    SLOT_NUMBER = "Dev.SlotNum"
    """Indicates the slot number in which this module is located in the chassis."""
    ETHERNET_IP_ADDRESS = "Dev.TCPIP.EthernetIP"
    """Indicates the IP address used to connect to the device. This will contain a blank string if hostname is used to connect to the chassis."""
    ETHERNET_MAC_ADDRESS = "Dev.TCPIP.EthernetMAC"
    """Indicates the MAC address of the device."""
    HOSTNAME = "Dev.TCPIP.Hostname"
    """Indicates the hostname used to connect to the chassis. This will contain a blank string if an IP address is used to connect to the chassis."""
    LAST_CONNECTED_ETHERNET_IP_ADDRESS = "Dev.TCPIP.LastConnectedEthernetIP"
    """Indicates the last connected IP address used to connect to the device."""
    VENDOR_NAME = "Dev.VendorName"
    """Indicates the vendor name for the device."""
    VENDOR_NUMBER = "Dev.VendorNum"
    """Indicates the NI-assigned vendor identification number for the device."""
    FIRMWARE_VERSION = "Dev.FirmwareVersion"
    """Indicates the fimware version for the device."""
    LAST_SCALING_CHANGE_TIME = "Dev.LastScalingChange"
    """Indicates the Last Scaling Change Timestamp in the module."""


class NVMEMAreaProperty(StrEnum):
    """Define SLSC NVMEMArea properties."""

    DESCRIPTION = "NVMEMArea.Descr"
    """Indicates a concise description of the NVMEM area, as a sentence fragment. This can be used to populate UI elements."""
    PENDING_CHANGES = "NVMEMArea.PendingChanges"
    """Indicates whether the session has pending changes for the NVMEM area."""
    SIZE = "NVMEMArea.Size"
    """Indicates the size of the NVMEM area, in bytes."""


class PhysicalChannelProperty(StrEnum):
    """Define SLSC PhysicalChannel properties."""

    COMMANDS = "PhysChan.Commands"
    """Indicates the names of physical channel commands defined by the device for this physical channel."""
    DESCRIPTION = "PhysChan.Descr"
    """Indicates a concise description of the physical channel, as a sentence fragment. This can be used to populate UI elements."""
    PROPERTIES = "PhysChan.Properties"
    """Indicates the names of physical channel properties defined by the device for this physical channel. Also see Sys.PhysChanProperties for driver-defined physical channel properties."""


class PropertyProperty(StrEnum):
    """Define SLSC Property properties."""

    DESCRIPTION = "Prop.Descr"
    """Indicates a concise description of the property, as a sentence fragment. This can be used to populate UI elements."""
    DOCUMENTATION = "Prop.Doc"
    """Indicates optional documentation for the property."""
    UNIT = "Prop.Unit"
    """Indicates the unit of the property."""
    MINIMUM_VALUE = "Prop.MinValue"
    """Indicates the minimum value of the property."""
    MAXIMUM_VALUE = "Prop.MaxValue"
    """Indicates the maximum value of the property."""
    ACCESS = "Prop.Access"
    """Indicates the access mode for the property."""
    DATA_TYPE = "Prop.DataType"
    """Indicates the data type for the property."""
    IS_ENUM = "Prop.IsEnum"
    """Indicates whether the property is an enum."""
    ENUM_NAME = "Prop.Enum.Name"
    """Indicates the enum name for the property."""
    ENUM_VALUE_NAMES = "Prop.Enum.ValueNames"
    """Indicates the enum value names for the property. Prop.Enum.ValueNames and Prop.EnumValues are parallel arrays."""
    ENUM_VALUES = "Prop.Enum.Values"
    """Indicates the enum value numbers for the property.  Prop.Enum.ValueNames and Prop.EnumValues are parallel arrays."""
    PENDING_CHANGES = "Prop.PendingChanges"
    """Indicates whether the session has pending changes for the property."""


class SessionProperty(StrEnum):
    """Define SLSC Session properties."""

    CONNECTED_DEVICES = "Session.ConnectedDevices"
    """Indicates which devices this session has network connections for. You can get this property as a string array or as a string containing a comma-delimited list of devices."""
    DEFAULT_DEVICES = "Session.DefaultDevices"
    """Specifies the default device(s) to use when the device name(s) input is not specified when calling the device and register VIs/functions. You can get/set this property as a string array or as a string containing a comma-delimited list of devices."""
    DEFAULT_NVMEM_AREAS = "Session.DefaultNVMEMAreas"
    """Specifies the default NVMEM area(s) to use when the NVMEM area(s) input is not specified when calling the NVMEM VIs/functions. You can get/set this property as a string array or as a string containing a comma-delimited list of NVMEM areas."""
    DEFAULT_PHYSICAL_CHANNELS = "Session.DefaultPhysChans"
    """Specifies the default physical channel(s) to use when the physical channel name(s) input is not specified when calling the physical channel VIs/functions. You can get/set this property as a string array or as a string containing a comma-delimited list of physical channels. Numbered physical channels may be specified as a colon-delimited range, such as ``Mod1/load0:3``."""
    RESERVED_DEVICES = "Session.ReservedDevices"
    """Indicates which devices are reserved by this session. You can get/set this property as a string array or as a string containing a comma-delimited list of devices."""
    RESERVATION_TIMEOUT = "Session.ReservationTimeout"
    """Specifies the timeout in seconds to wait for reservation to become available."""
    TCP_IP_CONNECT_TIMEOUT = "Session.TCPIP.ConnectTimeout"
    """Specifies the overall timeout for connecting to an SLSC chassis over the network, in seconds. When the session opens a network connection to an SLSC chassis, the session tries connecting using all known hostnames and IP addresses of the chassis until one succeeds or all have failed. If this timeout expires before a connection is successfully established, an error is returned. Some operations, such as DNS lookups, may not be abortable and may cause additional delays before a timeout error is returned."""
    TCP_IP_CONNECT_TIMEOUT_PER_IP_ADDRESS = "Session.TCPIP.ConnectTimeoutPerIP"
    """Specifies the timeout per IP address for connecting to an SLSC chassis over the network, in seconds. When the session opens a network connection to an SLSC chassis, the session tries connecting using all of the known hostnames and IP addresses of the chassis until one succeeds or all have failed. If this timeout expires before a connection to the current hostname or IP address is successfully established, the session moves on to the next hostname or IP address. The session will try each IP address once, even if multiple known hostnames resolve to that IP address. Some operations, such as DNS lookups, may not be abortable and may cause additional delays before the session moves on to the next hostname or IP addresss."""
    TCP_IP_MDNS_BROWSE_TIMEOUT = "Session.TCPIP.MDNSBrowseTimeout"
    """Specifies the timeout, in seconds, to wait for mDNS service instances to become available when connecting to devices."""
    TCP_IP_KEEP_ALIVE_TIMEOUT = "Session.TCPIP.KeepAliveTimeout"
    """Specifies the TCP keep-alive timeout, in seconds, for detecting when an SLSC chassis is disconnected from the network or powered off. If a network connection is idle long enough for the keep-alive timeout to expire, the operating system will periodically send keep-alive probe packets to the SLSC chassis. If the SLSC chassis does not respond after several probes, VIs/functions that access the network connection will begin to return errors. Setting this property only affects new network connections, not connections that are already open."""
    TCP_IP_KEEP_ALIVE_INTERVAL = "Session.TCPIP.KeepAliveInterval"
    """Specifies the TCP keep-alive interval, in seconds, for detecting when an SLSC chassis is disconnected from the network or powered off. When the operating system sends the SLSC chassis a keep-alive probe packet and the SLSC chassis does not respond, the keep-alive interval controls the rate at which the operating system retries the keep-alive probe. Setting this property only affects new network connections, not connections that are already open."""
    TCP_IP_SEND_RECEIVE_TIMEOUT = "Session.TCPIP.SendRecvTimeout"
    """Specifies the TCP send/receive timeout, in seconds. When the session sends a request to the SLSC chassis and the SLSC chassis does not reply before this timeout expires, an error is returned. Setting this property only affects new network connections, not connections that are already open."""


class SystemProperty(StrEnum):
    """Define SLSC System properties."""

    CHASSIS = "Sys.Chassis"
    """Indicates the names of the chassis available on the system."""
    CONFIG_CHANGE_COUNT = "Sys.ConfigChangeCount"
    """Per-session counter that increments when devices are added or removed. This allows you to cache the results of Sys.Chassis, Sys.Devices, and Sys.Modules, and to invalidate the cache when something changes. This property will always be greater than zero, and will increase when the configuration changes. Applications should not make assumptions about the initial value of this property, or the amount by which it will increase with each configuration change."""
    DEVICES = "Sys.Devices"
    """Indicates the names of the devices available on the system."""
    DEVICE_PROPERTIES = "Sys.DeviceProperties"
    """Indicates the names of the driver-defined device properties. Also see Dev.Properties for device-defined device properties."""
    MODULES = "Sys.Modules"
    """Indicates the names of the modules available on the system."""
    NVMEM_AREA_PROPERTIES = "Sys.NVMEMAreaProperties"
    """Indicates the names of the NVMEM area properties. All NVMEM area properties are driver-defined."""
    PHYSICAL_CHANNEL_PROPERTIES = "Sys.PhysChanProperties"
    """Indicates the names of the driver-defined physical channel properties. Also see PhysChan.Properties for device-defined physical channel properties."""
    SESSION_PROPERTIES = "Sys.SessionProperties"
    """Indicates the names of the session properties. All session properties are driver-defined."""
    SYSTEM_PROPERTIES = "Sys.SystemProperties"
    """Indicates the names of the system properties. All system properties are driver-defined."""


