"""SLSC Library Interpreter Implementation Module.

This module provides the LibraryInterpreter class, a concrete
implementation of the BaseInterpreter abstract interface that uses
ctypes to interface directly with the native SLSC C library.
"""

import ctypes
import warnings

from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language
from nislsc.error import SLSCError, SLSCWarning


lib = ctypes.CDLL("nislsc.dll")

lib.niSLSC_InitializeLibrary.restype = ctypes.c_int32
lib.niSLSC_InitializeLibrary.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_FinalizeLibrary.restype = ctypes.c_int32
lib.niSLSC_FinalizeLibrary.argtypes = [ctypes.c_void_p]

lib.niSLSC_GetLibraryVersion.restype = ctypes.c_int32
lib.niSLSC_GetLibraryVersion.argtypes = [ctypes.POINTER(ctypes.c_uint32)]

lib.niSLSC_GetExtendedErrorInfo.restype = ctypes.c_int32
lib.niSLSC_GetExtendedErrorInfo.argtypes = [ctypes.c_void_p, ctypes.c_int32, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetErrorDescription.restype = ctypes.c_int32
lib.niSLSC_GetErrorDescription.argtypes = [ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_FlattenNames.restype = ctypes.c_int32
lib.niSLSC_FlattenNames.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_UnflattenNames.restype = ctypes.c_int32
lib.niSLSC_UnflattenNames.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_InitializeSessionWithDevices.restype = ctypes.c_int32
lib.niSLSC_InitializeSessionWithDevices.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p, ctypes.c_double, ctypes.c_int32, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_InitializeSessionWithNVMEMAreas.restype = ctypes.c_int32
lib.niSLSC_InitializeSessionWithNVMEMAreas.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p, ctypes.c_double, ctypes.c_int32, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_InitializeSessionWithPhysicalChannels.restype = ctypes.c_int32
lib.niSLSC_InitializeSessionWithPhysicalChannels.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p, ctypes.c_double, ctypes.c_int32, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_InitializeSessionWithoutResources.restype = ctypes.c_int32
lib.niSLSC_InitializeSessionWithoutResources.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_CloseSession.restype = ctypes.c_int32
lib.niSLSC_CloseSession.argtypes = [ctypes.c_void_p]

lib.niSLSC_AbortSession.restype = ctypes.c_int32
lib.niSLSC_AbortSession.argtypes = [ctypes.c_void_p]

lib.niSLSC_LogIn.restype = ctypes.c_int32
lib.niSLSC_LogIn.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_bool]

lib.niSLSC_LogOut.restype = ctypes.c_int32
lib.niSLSC_LogOut.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_ConnectToDevices.restype = ctypes.c_int32
lib.niSLSC_ConnectToDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_DisconnectFromDevices.restype = ctypes.c_int32
lib.niSLSC_DisconnectFromDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_ConnectToChassisByAddress.restype = ctypes.c_int32
lib.niSLSC_ConnectToChassisByAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_ReserveDevices.restype = ctypes.c_int32
lib.niSLSC_ReserveDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int32, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_UnreserveDevices.restype = ctypes.c_int32
lib.niSLSC_UnreserveDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_ResetDevices.restype = ctypes.c_int32
lib.niSLSC_ResetDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_RenameDevice.restype = ctypes.c_int32
lib.niSLSC_RenameDevice.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_UpdateSystemConfigurationFile.restype = ctypes.c_int32
lib.niSLSC_UpdateSystemConfigurationFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_AddNetworkChassis.restype = ctypes.c_int32
lib.niSLSC_AddNetworkChassis.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_RemoveChassis.restype = ctypes.c_int32
lib.niSLSC_RemoveChassis.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_GetDevicePropertyBool.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]

lib.niSLSC_GetDevicePropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyDouble.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]

lib.niSLSC_GetDevicePropertyDoubleArray.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyDoubleArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyInt32.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]

lib.niSLSC_GetDevicePropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyInt64.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)]

lib.niSLSC_GetDevicePropertyInt64Array.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyString.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]

lib.niSLSC_GetDevicePropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetDevicePropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

lib.niSLSC_GetDevicePropertyUInt64Array.restype = ctypes.c_int32
lib.niSLSC_GetDevicePropertyUInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_SetDevicePropertyBool.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]

lib.niSLSC_SetDevicePropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t]

lib.niSLSC_SetDevicePropertyDouble.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_SetDevicePropertyDoubleArray.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyDoubleArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]

lib.niSLSC_SetDevicePropertyInt32.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]

lib.niSLSC_SetDevicePropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t]

lib.niSLSC_SetDevicePropertyInt64.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int64]

lib.niSLSC_SetDevicePropertyInt64Array.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t]

lib.niSLSC_SetDevicePropertyString.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetDevicePropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t]

lib.niSLSC_SetDevicePropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint32]

lib.niSLSC_SetDevicePropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t]

lib.niSLSC_SetDevicePropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]

lib.niSLSC_SetDevicePropertyUInt64Array.restype = ctypes.c_int32
lib.niSLSC_SetDevicePropertyUInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t]

lib.niSLSC_GetPhysicalChannelPropertyBool.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]

lib.niSLSC_GetPhysicalChannelPropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]

lib.niSLSC_GetPhysicalChannelPropertyDoubleArray.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyDoubleArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyInt32.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]

lib.niSLSC_GetPhysicalChannelPropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyInt64.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)]

lib.niSLSC_GetPhysicalChannelPropertyInt64Array.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyString.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]

lib.niSLSC_GetPhysicalChannelPropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPhysicalChannelPropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

lib.niSLSC_GetPhysicalChannelPropertyUInt64Array.restype = ctypes.c_int32
lib.niSLSC_GetPhysicalChannelPropertyUInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_SetPhysicalChannelPropertyBool.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]

lib.niSLSC_SetPhysicalChannelPropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t]

lib.niSLSC_SetPhysicalChannelPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_SetPhysicalChannelPropertyDoubleArray.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyDoubleArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]

lib.niSLSC_SetPhysicalChannelPropertyInt32.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]

lib.niSLSC_SetPhysicalChannelPropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t]

lib.niSLSC_SetPhysicalChannelPropertyInt64.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int64]

lib.niSLSC_SetPhysicalChannelPropertyInt64Array.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t]

lib.niSLSC_SetPhysicalChannelPropertyString.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetPhysicalChannelPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t]

lib.niSLSC_SetPhysicalChannelPropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint32]

lib.niSLSC_SetPhysicalChannelPropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t]

lib.niSLSC_SetPhysicalChannelPropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]

lib.niSLSC_SetPhysicalChannelPropertyUInt64Array.restype = ctypes.c_int32
lib.niSLSC_SetPhysicalChannelPropertyUInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t]

lib.niSLSC_CommitPropertiesForDevices.restype = ctypes.c_int32
lib.niSLSC_CommitPropertiesForDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_CommitPropertiesForPhysicalChannels.restype = ctypes.c_int32
lib.niSLSC_CommitPropertiesForPhysicalChannels.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_CommitPropertiesForSession.restype = ctypes.c_int32
lib.niSLSC_CommitPropertiesForSession.argtypes = [ctypes.c_void_p]

lib.niSLSC_CommitPropertiesGeneric.restype = ctypes.c_int32
lib.niSLSC_CommitPropertiesGeneric.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_GetNVMEMAreaPropertyBool.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMAreaPropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]

lib.niSLSC_GetNVMEMAreaPropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMAreaPropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetNVMEMAreaPropertyString.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMAreaPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetNVMEMAreaPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMAreaPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetNVMEMAreaPropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMAreaPropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]

lib.niSLSC_GetNVMEMAreaPropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMAreaPropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetSessionPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_GetSessionPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]

lib.niSLSC_GetSessionPropertyString.restype = ctypes.c_int32
lib.niSLSC_GetSessionPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetSessionPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetSessionPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_SetSessionPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_SetSessionPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_SetSessionPropertyString.restype = ctypes.c_int32
lib.niSLSC_SetSessionPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetSessionPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_SetSessionPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t]

lib.niSLSC_GetSystemPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_GetSystemPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]

lib.niSLSC_GetSystemPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetSystemPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetSystemPropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_GetSystemPropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

lib.niSLSC_SetSystemPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_SetSystemPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_GetGenericPropertyBool.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]

lib.niSLSC_GetGenericPropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]

lib.niSLSC_GetGenericPropertyDoubleArray.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyDoubleArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyInt32.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]

lib.niSLSC_GetGenericPropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyInt64.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)]

lib.niSLSC_GetGenericPropertyInt64Array.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyString.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]

lib.niSLSC_GetGenericPropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetGenericPropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64)]

lib.niSLSC_GetGenericPropertyUInt64Array.restype = ctypes.c_int32
lib.niSLSC_GetGenericPropertyUInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_SetGenericPropertyBool.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]

lib.niSLSC_SetGenericPropertyBoolArray.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t]

lib.niSLSC_SetGenericPropertyDouble.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyDouble.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_SetGenericPropertyDoubleArray.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyDoubleArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]

lib.niSLSC_SetGenericPropertyInt32.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]

lib.niSLSC_SetGenericPropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t]

lib.niSLSC_SetGenericPropertyInt64.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int64]

lib.niSLSC_SetGenericPropertyInt64Array.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64), ctypes.c_size_t]

lib.niSLSC_SetGenericPropertyString.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetGenericPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t]

lib.niSLSC_SetGenericPropertyUInt32.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint32]

lib.niSLSC_SetGenericPropertyUInt32Array.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyUInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_size_t]

lib.niSLSC_SetGenericPropertyUInt64.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]

lib.niSLSC_SetGenericPropertyUInt64Array.restype = ctypes.c_int32
lib.niSLSC_SetGenericPropertyUInt64Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t]

lib.niSLSC_ExecuteDeviceCommand.restype = ctypes.c_int32
lib.niSLSC_ExecuteDeviceCommand.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_ExecutePhysicalChannelCommand.restype = ctypes.c_int32
lib.niSLSC_ExecutePhysicalChannelCommand.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_ExecuteGenericCommand.restype = ctypes.c_int32
lib.niSLSC_ExecuteGenericCommand.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]

lib.niSLSC_ReadRegisterUInt8.restype = ctypes.c_int32
lib.niSLSC_ReadRegisterUInt8.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8)]

lib.niSLSC_ReadRegisterUInt16.restype = ctypes.c_int32
lib.niSLSC_ReadRegisterUInt16.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint16)]

lib.niSLSC_ReadRegisterUInt32.restype = ctypes.c_int32
lib.niSLSC_ReadRegisterUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]

lib.niSLSC_ReadRegisterUInt64.restype = ctypes.c_int32
lib.niSLSC_ReadRegisterUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint64)]

lib.niSLSC_WriteRegisterUInt8.restype = ctypes.c_int32
lib.niSLSC_WriteRegisterUInt8.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint8]

lib.niSLSC_WriteRegisterUInt16.restype = ctypes.c_int32
lib.niSLSC_WriteRegisterUInt16.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint16]

lib.niSLSC_WriteRegisterUInt32.restype = ctypes.c_int32
lib.niSLSC_WriteRegisterUInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32]

lib.niSLSC_WriteRegisterUInt64.restype = ctypes.c_int32
lib.niSLSC_WriteRegisterUInt64.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint64]

lib.niSLSC_GetNVMEMBytes.restype = ctypes.c_int32
lib.niSLSC_GetNVMEMBytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]

lib.niSLSC_SetNVMEMBytes.restype = ctypes.c_int32
lib.niSLSC_SetNVMEMBytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_CommitNVMEMAreas.restype = ctypes.c_int32
lib.niSLSC_CommitNVMEMAreas.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_CommitNVMEMForDevices.restype = ctypes.c_int32
lib.niSLSC_CommitNVMEMForDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_CommitNVMEMForSession.restype = ctypes.c_int32
lib.niSLSC_CommitNVMEMForSession.argtypes = [ctypes.c_void_p]

lib.niSLSC_CommitNVMEMGeneric.restype = ctypes.c_int32
lib.niSLSC_CommitNVMEMGeneric.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_GetLinearScalingParameters.restype = ctypes.c_int32
lib.niSLSC_GetLinearScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

lib.niSLSC_GetPolynomialScalingParameters.restype = ctypes.c_int32
lib.niSLSC_GetPolynomialScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetTableScalingParameters.restype = ctypes.c_int32
lib.niSLSC_GetTableScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_int32)]

lib.niSLSC_GetUserDefinedScalingParameters.restype = ctypes.c_int32
lib.niSLSC_GetUserDefinedScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetUserDefinedScalingEquation.restype = ctypes.c_int32
lib.niSLSC_GetUserDefinedScalingEquation.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_SetLinearScalingParameters.restype = ctypes.c_int32
lib.niSLSC_SetLinearScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetPolynomialScalingParameters.restype = ctypes.c_int32
lib.niSLSC_SetPolynomialScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetTableScalingParameters.restype = ctypes.c_int32
lib.niSLSC_SetTableScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.c_int32, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetUserDefinedScalingParameters.restype = ctypes.c_int32
lib.niSLSC_SetUserDefinedScalingParameters.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t, ctypes.POINTER(ctypes.c_double), ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_SetUserDefinedScalingEquation.restype = ctypes.c_int32
lib.niSLSC_SetUserDefinedScalingEquation.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

lib.niSLSC_CommitScalingForDevices.restype = ctypes.c_int32
lib.niSLSC_CommitScalingForDevices.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

lib.niSLSC_OpenDeviceCommand.restype = ctypes.c_int32
lib.niSLSC_OpenDeviceCommand.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_OpenPhysicalChannelCommand.restype = ctypes.c_int32
lib.niSLSC_OpenPhysicalChannelCommand.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_OpenGenericCommand.restype = ctypes.c_int32
lib.niSLSC_OpenGenericCommand.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_CloseCommand.restype = ctypes.c_int32
lib.niSLSC_CloseCommand.argtypes = [ctypes.c_void_p]

lib.niSLSC_GetCommandPropertyString.restype = ctypes.c_int32
lib.niSLSC_GetCommandPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_OpenDeviceProperty.restype = ctypes.c_int32
lib.niSLSC_OpenDeviceProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_OpenPhysicalChannelProperty.restype = ctypes.c_int32
lib.niSLSC_OpenPhysicalChannelProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_OpenDriverDefinedProperty.restype = ctypes.c_int32
lib.niSLSC_OpenDriverDefinedProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_OpenGenericProperty.restype = ctypes.c_int32
lib.niSLSC_OpenGenericProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

lib.niSLSC_CloseProperty.restype = ctypes.c_int32
lib.niSLSC_CloseProperty.argtypes = [ctypes.c_void_p]

lib.niSLSC_GetPropertyPropertyBool.restype = ctypes.c_int32
lib.niSLSC_GetPropertyPropertyBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]

lib.niSLSC_GetPropertyPropertyInt32.restype = ctypes.c_int32
lib.niSLSC_GetPropertyPropertyInt32.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]

lib.niSLSC_GetPropertyPropertyInt32Array.restype = ctypes.c_int32
lib.niSLSC_GetPropertyPropertyInt32Array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPropertyPropertyString.restype = ctypes.c_int32
lib.niSLSC_GetPropertyPropertyString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

lib.niSLSC_GetPropertyPropertyStringArray.restype = ctypes.c_int32
lib.niSLSC_GetPropertyPropertyStringArray.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]

class LibraryInterpreter(BaseInterpreter):

    def initialize_library(self, version: int) -> int:
        version_c = ctypes.c_uint32(version)
        library_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_InitializeLibrary(version_c, ctypes.byref(library_handle_c))
        self.check_for_code(status)
        return library_handle_c.value or 0

    def finalize_library(self, library_handle: int) -> None:
        library_handle_c = ctypes.c_void_p(library_handle)
        status = lib.niSLSC_FinalizeLibrary(library_handle_c)
        self.check_for_code(status)
        return 

    def get_library_version(self) -> int:
        version_c = ctypes.c_uint32()
        status = lib.niSLSC_GetLibraryVersion(ctypes.byref(version_c))
        self.check_for_code(status)
        return version_c.value

    def get_extended_error_info(self, library_handle: int, language: Language) -> str:
        library_handle_c = ctypes.c_void_p(library_handle)
        language_c = ctypes.c_int32(language.value)
        extended_error_info_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetExtendedErrorInfo(library_handle_c, language_c, None, 0, ctypes.byref(extended_error_info_actual_size))
        if extended_error_info_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(extended_error_info_actual_size.value)
        status = lib.niSLSC_GetExtendedErrorInfo(library_handle_c, language_c, buffer, extended_error_info_actual_size.value, None)
        self.check_for_code(status)
        extended_error_info_value = buffer.value.decode('utf-8')
        return extended_error_info_value

    def get_error_description(self, library_handle: int, status_code: int, language: Language) -> str:
        library_handle_c = ctypes.c_void_p(library_handle)
        status_code_c = ctypes.c_int32(status_code)
        language_c = ctypes.c_int32(language.value)
        error_description_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetErrorDescription(library_handle_c, status_code_c, language_c, None, 0, ctypes.byref(error_description_actual_size))
        if error_description_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(error_description_actual_size.value)
        status = lib.niSLSC_GetErrorDescription(library_handle_c, status_code_c, language_c, buffer, error_description_actual_size.value, None)
        self.check_for_code(status)
        error_description_value = buffer.value.decode('utf-8')
        return error_description_value

    def flatten_names(self, names_in: list[str]) -> str:
        names_in_bytes = [string.encode('utf-8') for string in names_in]
        array_type = ctypes.c_char_p * len(names_in_bytes)
        names_in_array = array_type(*names_in_bytes)
        names_out_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_FlattenNames(names_in_array, ctypes.c_size_t(len(names_in_bytes)), None, 0, ctypes.byref(names_out_actual_size))
        if names_out_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(names_out_actual_size.value)
        status = lib.niSLSC_FlattenNames(names_in_array, ctypes.c_size_t(len(names_in_bytes)), buffer, names_out_actual_size.value, None)
        self.check_for_code(status)
        names_out_value = buffer.value.decode('utf-8')
        return names_out_value

    def unflatten_names(self, names_in: str) -> list[str]:
        names_in_bytes = names_in.encode('utf-8')
        names_out_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_names_out = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_UnflattenNames(names_in_bytes, ctypes.byref(names_out_ptr), ctypes.byref(num_names_out), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_UnflattenNames(names_in_bytes, ctypes.byref(names_out_ptr), ctypes.byref(num_names_out), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        names_out_array = []
        for i in range(num_names_out.value):
            names_out_array.append(ctypes.string_at(names_out_ptr[i]).decode('utf-8'))
        return names_out_array

    def initialize_session_with_devices(self, library_handle: int, device_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int:
        library_handle_c = ctypes.c_void_p(library_handle)
        session_handle_c = ctypes.c_void_p()
        device_names_bytes = device_names.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        reservation_access_c = ctypes.c_int32(reservation_access)
        reservation_group_bytes = reservation_group.encode('utf-8')
        reservation_timeout_c = ctypes.c_double(reservation_timeout)
        status = lib.niSLSC_InitializeSessionWithDevices(library_handle_c, ctypes.byref(session_handle_c), device_names_bytes, connection_timeout_c, reservation_access_c, reservation_group_bytes, reservation_timeout_c)
        self.check_for_code(status)
        return session_handle_c.value or 0

    def initialize_session_with_nvmem_areas(self, library_handle: int, nvmem_area_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int:
        library_handle_c = ctypes.c_void_p(library_handle)
        session_handle_c = ctypes.c_void_p()
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        reservation_access_c = ctypes.c_int32(reservation_access)
        reservation_group_bytes = reservation_group.encode('utf-8')
        reservation_timeout_c = ctypes.c_double(reservation_timeout)
        status = lib.niSLSC_InitializeSessionWithNVMEMAreas(library_handle_c, ctypes.byref(session_handle_c), nvmem_area_names_bytes, connection_timeout_c, reservation_access_c, reservation_group_bytes, reservation_timeout_c)
        self.check_for_code(status)
        return session_handle_c.value or 0

    def initialize_session_with_physical_channels(self, library_handle: int, physical_channel_names: str, connection_timeout: float, reservation_access: int, reservation_group: str, reservation_timeout: float) -> int:
        library_handle_c = ctypes.c_void_p(library_handle)
        session_handle_c = ctypes.c_void_p()
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        reservation_access_c = ctypes.c_int32(reservation_access)
        reservation_group_bytes = reservation_group.encode('utf-8')
        reservation_timeout_c = ctypes.c_double(reservation_timeout)
        status = lib.niSLSC_InitializeSessionWithPhysicalChannels(library_handle_c, ctypes.byref(session_handle_c), physical_channel_names_bytes, connection_timeout_c, reservation_access_c, reservation_group_bytes, reservation_timeout_c)
        self.check_for_code(status)
        return session_handle_c.value or 0

    def initialize_session_without_resources(self, library_handle: int) -> int:
        library_handle_c = ctypes.c_void_p(library_handle)
        session_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_InitializeSessionWithoutResources(library_handle_c, ctypes.byref(session_handle_c))
        self.check_for_code(status)
        return session_handle_c.value or 0

    def close_session(self, session_handle: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        status = lib.niSLSC_CloseSession(session_handle_c)
        self.check_for_code(status)
        return 

    def abort_session(self, session_handle: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        status = lib.niSLSC_AbortSession(session_handle_c)
        self.check_for_code(status)
        return 

    def log_in(self, session_handle: int, chassis_name: str, username: str, password: str, connection_timeout: float, save_credentials_to_disk: bool) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        chassis_name_bytes = chassis_name.encode('utf-8')
        username_bytes = username.encode('utf-8')
        password_bytes = password.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        save_credentials_to_disk_c = ctypes.c_bool(save_credentials_to_disk)
        status = lib.niSLSC_LogIn(session_handle_c, chassis_name_bytes, username_bytes, password_bytes, connection_timeout_c, save_credentials_to_disk_c)
        self.check_for_code(status)
        return 

    def log_out(self, session_handle: int, chassis_name: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        chassis_name_bytes = chassis_name.encode('utf-8')
        status = lib.niSLSC_LogOut(session_handle_c, chassis_name_bytes)
        self.check_for_code(status)
        return 

    def connect_to_devices(self, session_handle: int, device_names: str, connection_timeout: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        status = lib.niSLSC_ConnectToDevices(session_handle_c, device_names_bytes, connection_timeout_c)
        self.check_for_code(status)
        return 

    def disconnect_from_devices(self, session_handle: int, device_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        status = lib.niSLSC_DisconnectFromDevices(session_handle_c, device_names_bytes)
        self.check_for_code(status)
        return 

    def connect_to_chassis_by_address(self, session_handle: int, address: str, username: str, password: str, connection_timeout: float) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        address_bytes = address.encode('utf-8')
        username_bytes = username.encode('utf-8')
        password_bytes = password.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        chassis_name_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_ConnectToChassisByAddress(session_handle_c, address_bytes, username_bytes, password_bytes, connection_timeout_c, None, 0, ctypes.byref(chassis_name_actual_size))
        if chassis_name_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(chassis_name_actual_size.value)
        status = lib.niSLSC_ConnectToChassisByAddress(session_handle_c, address_bytes, username_bytes, password_bytes, connection_timeout_c, buffer, chassis_name_actual_size.value, None)
        self.check_for_code(status)
        chassis_name_value = buffer.value.decode('utf-8')
        return chassis_name_value

    def reserve_devices(self, session_handle: int, device_names: str, reservation_access: int, reservation_group: str, reservation_timeout: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        reservation_access_c = ctypes.c_int32(reservation_access)
        reservation_group_bytes = reservation_group.encode('utf-8')
        reservation_timeout_c = ctypes.c_double(reservation_timeout)
        status = lib.niSLSC_ReserveDevices(session_handle_c, device_names_bytes, reservation_access_c, reservation_group_bytes, reservation_timeout_c)
        self.check_for_code(status)
        return 

    def unreserve_devices(self, session_handle: int, device_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        status = lib.niSLSC_UnreserveDevices(session_handle_c, device_names_bytes)
        self.check_for_code(status)
        return 

    def reset_devices(self, session_handle: int, device_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        status = lib.niSLSC_ResetDevices(session_handle_c, device_names_bytes)
        self.check_for_code(status)
        return 

    def rename_device(self, session_handle: int, device_name: str, new_device_name: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        new_device_name_bytes = new_device_name.encode('utf-8')
        status = lib.niSLSC_RenameDevice(session_handle_c, device_name_bytes, new_device_name_bytes)
        self.check_for_code(status)
        return 

    def update_system_configuration_file(self, session_handle: int, chassis_name: str, connection_timeout: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        chassis_name_bytes = chassis_name.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        status = lib.niSLSC_UpdateSystemConfigurationFile(session_handle_c, chassis_name_bytes, connection_timeout_c)
        self.check_for_code(status)
        return 

    def add_network_chassis(self, session_handle: int, address: str, username: str, password: str, connection_timeout: float) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        address_bytes = address.encode('utf-8')
        username_bytes = username.encode('utf-8')
        password_bytes = password.encode('utf-8')
        connection_timeout_c = ctypes.c_double(connection_timeout)
        chassis_name_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_AddNetworkChassis(session_handle_c, address_bytes, username_bytes, password_bytes, connection_timeout_c, None, 0, ctypes.byref(chassis_name_actual_size))
        if chassis_name_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(chassis_name_actual_size.value)
        status = lib.niSLSC_AddNetworkChassis(session_handle_c, address_bytes, username_bytes, password_bytes, connection_timeout_c, buffer, chassis_name_actual_size.value, None)
        self.check_for_code(status)
        chassis_name_value = buffer.value.decode('utf-8')
        return chassis_name_value

    def remove_chassis(self, session_handle: int, chassis_name: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        chassis_name_bytes = chassis_name.encode('utf-8')
        status = lib.niSLSC_RemoveChassis(session_handle_c, chassis_name_bytes)
        self.check_for_code(status)
        return 

    def get_device_property_bool(self, session_handle: int, device_names: str, property_name: str) -> bool:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool()
        status = lib.niSLSC_GetDevicePropertyBool(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_device_property_bool_array(self, session_handle: int, device_names: str, property_name: str) -> list[bool]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyBoolArray(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_bool * property_value_actual_size.value)()
        status = lib.niSLSC_GetDevicePropertyBoolArray(session_handle_c, device_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_device_property_double(self, session_handle: int, device_names: str, property_name: str) -> float:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double()
        status = lib.niSLSC_GetDevicePropertyDouble(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_device_property_double_array(self, session_handle: int, device_names: str, property_name: str) -> list[float]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyDoubleArray(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_double * property_value_actual_size.value)()
        status = lib.niSLSC_GetDevicePropertyDoubleArray(session_handle_c, device_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_device_property_int32(self, session_handle: int, device_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32()
        status = lib.niSLSC_GetDevicePropertyInt32(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_device_property_int32_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyInt32Array(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetDevicePropertyInt32Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_device_property_int64(self, session_handle: int, device_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int64()
        status = lib.niSLSC_GetDevicePropertyInt64(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_device_property_int64_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyInt64Array(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int64 * property_value_actual_size.value)()
        status = lib.niSLSC_GetDevicePropertyInt64Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_device_property_string(self, session_handle: int, device_names: str, property_name: str) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyString(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetDevicePropertyString(session_handle_c, device_names_bytes, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def get_device_property_string_array(self, session_handle: int, device_names: str, property_name: str) -> list[str]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyStringArray(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetDevicePropertyStringArray(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def get_device_property_uint32(self, session_handle: int, device_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32()
        status = lib.niSLSC_GetDevicePropertyUInt32(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_device_property_uint32_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyUInt32Array(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetDevicePropertyUInt32Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_device_property_uint64(self, session_handle: int, device_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64()
        status = lib.niSLSC_GetDevicePropertyUInt64(session_handle_c, device_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_device_property_uint64_array(self, session_handle: int, device_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetDevicePropertyUInt64Array(session_handle_c, device_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint64 * property_value_actual_size.value)()
        status = lib.niSLSC_GetDevicePropertyUInt64Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def set_device_property_bool(self, session_handle: int, device_names: str, property_name: str, property_value: bool) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool(property_value)
        status = lib.niSLSC_SetDevicePropertyBool(session_handle_c, device_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_device_property_bool_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[bool]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_bool * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetDevicePropertyBoolArray(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_device_property_double(self, session_handle: int, device_names: str, property_name: str, property_value: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double(property_value)
        status = lib.niSLSC_SetDevicePropertyDouble(session_handle_c, device_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_device_property_double_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[float]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_double * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetDevicePropertyDoubleArray(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_device_property_int32(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32(property_value)
        status = lib.niSLSC_SetDevicePropertyInt32(session_handle_c, device_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_device_property_int32_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_int32 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetDevicePropertyInt32Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_device_property_int64(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int64(property_value)
        status = lib.niSLSC_SetDevicePropertyInt64(session_handle_c, device_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_device_property_int64_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_int64 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetDevicePropertyInt64Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_device_property_string(self, session_handle: int, device_names: str, property_name: str, property_value: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = property_value.encode('utf-8')
        status = lib.niSLSC_SetDevicePropertyString(session_handle_c, device_names_bytes, property_name_bytes, property_value_bytes)
        self.check_for_code(status)
        return 

    def set_device_property_string_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[str]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = [string.encode('utf-8') for string in property_value]
        array_type = ctypes.c_char_p * len(property_value_bytes)
        property_value_array = array_type(*property_value_bytes)
        status = lib.niSLSC_SetDevicePropertyStringArray(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, ctypes.c_size_t(len(property_value_bytes)))
        self.check_for_code(status)
        return 

    def set_device_property_uint32(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32(property_value)
        status = lib.niSLSC_SetDevicePropertyUInt32(session_handle_c, device_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_device_property_uint32_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_uint32 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetDevicePropertyUInt32Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_device_property_uint64(self, session_handle: int, device_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64(property_value)
        status = lib.niSLSC_SetDevicePropertyUInt64(session_handle_c, device_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_device_property_uint64_array(self, session_handle: int, device_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_uint64 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetDevicePropertyUInt64Array(session_handle_c, device_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def get_physical_channel_property_bool(self, session_handle: int, physical_channel_names: str, property_name: str) -> bool:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool()
        status = lib.niSLSC_GetPhysicalChannelPropertyBool(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_physical_channel_property_bool_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[bool]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyBoolArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_bool * property_value_actual_size.value)()
        status = lib.niSLSC_GetPhysicalChannelPropertyBoolArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_physical_channel_property_double(self, session_handle: int, physical_channel_names: str, property_name: str) -> float:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double()
        status = lib.niSLSC_GetPhysicalChannelPropertyDouble(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_physical_channel_property_double_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[float]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyDoubleArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_double * property_value_actual_size.value)()
        status = lib.niSLSC_GetPhysicalChannelPropertyDoubleArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_physical_channel_property_int32(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32()
        status = lib.niSLSC_GetPhysicalChannelPropertyInt32(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_physical_channel_property_int32_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyInt32Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetPhysicalChannelPropertyInt32Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_physical_channel_property_int64(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int64()
        status = lib.niSLSC_GetPhysicalChannelPropertyInt64(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_physical_channel_property_int64_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyInt64Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int64 * property_value_actual_size.value)()
        status = lib.niSLSC_GetPhysicalChannelPropertyInt64Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_physical_channel_property_string(self, session_handle: int, physical_channel_names: str, property_name: str) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyString(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetPhysicalChannelPropertyString(session_handle_c, physical_channel_names_bytes, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def get_physical_channel_property_string_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[str]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyStringArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetPhysicalChannelPropertyStringArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def get_physical_channel_property_uint32(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32()
        status = lib.niSLSC_GetPhysicalChannelPropertyUInt32(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_physical_channel_property_uint32_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyUInt32Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetPhysicalChannelPropertyUInt32Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_physical_channel_property_uint64(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64()
        status = lib.niSLSC_GetPhysicalChannelPropertyUInt64(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_physical_channel_property_uint64_array(self, session_handle: int, physical_channel_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPhysicalChannelPropertyUInt64Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint64 * property_value_actual_size.value)()
        status = lib.niSLSC_GetPhysicalChannelPropertyUInt64Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def set_physical_channel_property_bool(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: bool) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyBool(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_bool_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[bool]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_bool * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyBoolArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_double(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyDouble(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_double_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[float]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_double * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyDoubleArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_int32(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyInt32(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_int32_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_int32 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyInt32Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_int64(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int64(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyInt64(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_int64_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_int64 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyInt64Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_string(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = property_value.encode('utf-8')
        status = lib.niSLSC_SetPhysicalChannelPropertyString(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_bytes)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_string_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[str]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = [string.encode('utf-8') for string in property_value]
        array_type = ctypes.c_char_p * len(property_value_bytes)
        property_value_array = array_type(*property_value_bytes)
        status = lib.niSLSC_SetPhysicalChannelPropertyStringArray(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, ctypes.c_size_t(len(property_value_bytes)))
        self.check_for_code(status)
        return 

    def set_physical_channel_property_uint32(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyUInt32(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_uint32_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_uint32 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyUInt32Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_uint64(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyUInt64(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_physical_channel_property_uint64_array(self, session_handle: int, physical_channel_names: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_uint64 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetPhysicalChannelPropertyUInt64Array(session_handle_c, physical_channel_names_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def commit_properties_for_devices(self, session_handle: int, device_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        status = lib.niSLSC_CommitPropertiesForDevices(session_handle_c, device_names_bytes)
        self.check_for_code(status)
        return 

    def commit_properties_for_physical_channels(self, session_handle: int, physical_channel_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        status = lib.niSLSC_CommitPropertiesForPhysicalChannels(session_handle_c, physical_channel_names_bytes)
        self.check_for_code(status)
        return 

    def commit_properties_for_session(self, session_handle: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        status = lib.niSLSC_CommitPropertiesForSession(session_handle_c)
        self.check_for_code(status)
        return 

    def commit_properties_generic(self, session_handle: int, resources: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        status = lib.niSLSC_CommitPropertiesGeneric(session_handle_c, resources_bytes)
        self.check_for_code(status)
        return 

    def get_nvmem_area_property_bool(self, session_handle: int, nvmem_area_names: str, property_name: str) -> bool:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool()
        status = lib.niSLSC_GetNVMEMAreaPropertyBool(session_handle_c, nvmem_area_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_nvmem_area_property_bool_array(self, session_handle: int, nvmem_area_names: str, property_name: str) -> list[bool]:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetNVMEMAreaPropertyBoolArray(session_handle_c, nvmem_area_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_bool * property_value_actual_size.value)()
        status = lib.niSLSC_GetNVMEMAreaPropertyBoolArray(session_handle_c, nvmem_area_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_nvmem_area_property_string(self, session_handle: int, nvmem_area_names: str, property_name: str) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetNVMEMAreaPropertyString(session_handle_c, nvmem_area_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetNVMEMAreaPropertyString(session_handle_c, nvmem_area_names_bytes, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def get_nvmem_area_property_string_array(self, session_handle: int, nvmem_area_names: str, property_name: str) -> list[str]:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetNVMEMAreaPropertyStringArray(session_handle_c, nvmem_area_names_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetNVMEMAreaPropertyStringArray(session_handle_c, nvmem_area_names_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def get_nvmem_area_property_uint32(self, session_handle: int, nvmem_area_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32()
        status = lib.niSLSC_GetNVMEMAreaPropertyUInt32(session_handle_c, nvmem_area_names_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_nvmem_area_property_uint32_array(self, session_handle: int, nvmem_area_names: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetNVMEMAreaPropertyUInt32Array(session_handle_c, nvmem_area_names_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetNVMEMAreaPropertyUInt32Array(session_handle_c, nvmem_area_names_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_session_property_double(self, session_handle: int, property_name: str) -> float:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double()
        status = lib.niSLSC_GetSessionPropertyDouble(session_handle_c, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_session_property_string(self, session_handle: int, property_name: str) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetSessionPropertyString(session_handle_c, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetSessionPropertyString(session_handle_c, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def get_session_property_string_array(self, session_handle: int, property_name: str) -> list[str]:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetSessionPropertyStringArray(session_handle_c, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetSessionPropertyStringArray(session_handle_c, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def set_session_property_double(self, session_handle: int, property_name: str, property_value: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double(property_value)
        status = lib.niSLSC_SetSessionPropertyDouble(session_handle_c, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_session_property_string(self, session_handle: int, property_name: str, property_value: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = property_value.encode('utf-8')
        status = lib.niSLSC_SetSessionPropertyString(session_handle_c, property_name_bytes, property_value_bytes)
        self.check_for_code(status)
        return 

    def set_session_property_string_array(self, session_handle: int, property_name: str, property_value: list[str]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = [string.encode('utf-8') for string in property_value]
        array_type = ctypes.c_char_p * len(property_value_bytes)
        property_value_array = array_type(*property_value_bytes)
        status = lib.niSLSC_SetSessionPropertyStringArray(session_handle_c, property_name_bytes, property_value_array, ctypes.c_size_t(len(property_value_bytes)))
        self.check_for_code(status)
        return 

    def get_system_property_double(self, session_handle: int, property_name: str) -> float:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double()
        status = lib.niSLSC_GetSystemPropertyDouble(session_handle_c, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_system_property_string_array(self, session_handle: int, property_name: str) -> list[str]:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetSystemPropertyStringArray(session_handle_c, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetSystemPropertyStringArray(session_handle_c, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def get_system_property_uint64(self, session_handle: int, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64()
        status = lib.niSLSC_GetSystemPropertyUInt64(session_handle_c, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def set_system_property_double(self, session_handle: int, property_name: str, property_value: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double(property_value)
        status = lib.niSLSC_SetSystemPropertyDouble(session_handle_c, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def get_generic_property_bool(self, session_handle: int, resources: str, property_name: str) -> bool:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool()
        status = lib.niSLSC_GetGenericPropertyBool(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_generic_property_bool_array(self, session_handle: int, resources: str, property_name: str) -> list[bool]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyBoolArray(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_bool * property_value_actual_size.value)()
        status = lib.niSLSC_GetGenericPropertyBoolArray(session_handle_c, resources_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_generic_property_double(self, session_handle: int, resources: str, property_name: str) -> float:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double()
        status = lib.niSLSC_GetGenericPropertyDouble(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_generic_property_double_array(self, session_handle: int, resources: str, property_name: str) -> list[float]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyDoubleArray(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_double * property_value_actual_size.value)()
        status = lib.niSLSC_GetGenericPropertyDoubleArray(session_handle_c, resources_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_generic_property_int32(self, session_handle: int, resources: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32()
        status = lib.niSLSC_GetGenericPropertyInt32(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_generic_property_int32_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyInt32Array(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetGenericPropertyInt32Array(session_handle_c, resources_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_generic_property_int64(self, session_handle: int, resources: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int64()
        status = lib.niSLSC_GetGenericPropertyInt64(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_generic_property_int64_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyInt64Array(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int64 * property_value_actual_size.value)()
        status = lib.niSLSC_GetGenericPropertyInt64Array(session_handle_c, resources_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_generic_property_string(self, session_handle: int, resources: str, property_name: str) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyString(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetGenericPropertyString(session_handle_c, resources_bytes, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def get_generic_property_string_array(self, session_handle: int, resources: str, property_name: str) -> list[str]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyStringArray(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetGenericPropertyStringArray(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def get_generic_property_uint32(self, session_handle: int, resources: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32()
        status = lib.niSLSC_GetGenericPropertyUInt32(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_generic_property_uint32_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyUInt32Array(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetGenericPropertyUInt32Array(session_handle_c, resources_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_generic_property_uint64(self, session_handle: int, resources: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64()
        status = lib.niSLSC_GetGenericPropertyUInt64(session_handle_c, resources_bytes, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_generic_property_uint64_array(self, session_handle: int, resources: str, property_name: str) -> list[int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetGenericPropertyUInt64Array(session_handle_c, resources_bytes, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_uint64 * property_value_actual_size.value)()
        status = lib.niSLSC_GetGenericPropertyUInt64Array(session_handle_c, resources_bytes, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def set_generic_property_bool(self, session_handle: int, resources: str, property_name: str, property_value: bool) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool(property_value)
        status = lib.niSLSC_SetGenericPropertyBool(session_handle_c, resources_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_generic_property_bool_array(self, session_handle: int, resources: str, property_name: str, property_value: list[bool]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_bool * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetGenericPropertyBoolArray(session_handle_c, resources_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_generic_property_double(self, session_handle: int, resources: str, property_name: str, property_value: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_double(property_value)
        status = lib.niSLSC_SetGenericPropertyDouble(session_handle_c, resources_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_generic_property_double_array(self, session_handle: int, resources: str, property_name: str, property_value: list[float]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_double * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetGenericPropertyDoubleArray(session_handle_c, resources_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_generic_property_int32(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32(property_value)
        status = lib.niSLSC_SetGenericPropertyInt32(session_handle_c, resources_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_generic_property_int32_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_int32 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetGenericPropertyInt32Array(session_handle_c, resources_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_generic_property_int64(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int64(property_value)
        status = lib.niSLSC_SetGenericPropertyInt64(session_handle_c, resources_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_generic_property_int64_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_int64 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetGenericPropertyInt64Array(session_handle_c, resources_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_generic_property_string(self, session_handle: int, resources: str, property_name: str, property_value: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = property_value.encode('utf-8')
        status = lib.niSLSC_SetGenericPropertyString(session_handle_c, resources_bytes, property_name_bytes, property_value_bytes)
        self.check_for_code(status)
        return 

    def set_generic_property_string_array(self, session_handle: int, resources: str, property_name: str, property_value: list[str]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_bytes = [string.encode('utf-8') for string in property_value]
        array_type = ctypes.c_char_p * len(property_value_bytes)
        property_value_array = array_type(*property_value_bytes)
        status = lib.niSLSC_SetGenericPropertyStringArray(session_handle_c, resources_bytes, property_name_bytes, property_value_array, ctypes.c_size_t(len(property_value_bytes)))
        self.check_for_code(status)
        return 

    def set_generic_property_uint32(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint32(property_value)
        status = lib.niSLSC_SetGenericPropertyUInt32(session_handle_c, resources_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_generic_property_uint32_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_uint32 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetGenericPropertyUInt32Array(session_handle_c, resources_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def set_generic_property_uint64(self, session_handle: int, resources: str, property_name: str, property_value: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_uint64(property_value)
        status = lib.niSLSC_SetGenericPropertyUInt64(session_handle_c, resources_bytes, property_name_bytes, property_value_c)
        self.check_for_code(status)
        return 

    def set_generic_property_uint64_array(self, session_handle: int, resources: str, property_name: str, property_value: list[int]) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_value_array = (ctypes.c_uint64 * len(property_value))(*property_value)
        property_value_array_size = len(property_value)
        status = lib.niSLSC_SetGenericPropertyUInt64Array(session_handle_c, resources_bytes, property_name_bytes, property_value_array, property_value_array_size)
        self.check_for_code(status)
        return 

    def execute_device_command(self, session_handle: int, device_names: str, command_name: str, timeout: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        command_name_bytes = command_name.encode('utf-8')
        timeout_c = ctypes.c_double(timeout)
        status = lib.niSLSC_ExecuteDeviceCommand(session_handle_c, device_names_bytes, command_name_bytes, timeout_c)
        self.check_for_code(status)
        return 

    def execute_physical_channel_command(self, session_handle: int, physical_channel_names: str, command_name: str, timeout: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        command_name_bytes = command_name.encode('utf-8')
        timeout_c = ctypes.c_double(timeout)
        status = lib.niSLSC_ExecutePhysicalChannelCommand(session_handle_c, physical_channel_names_bytes, command_name_bytes, timeout_c)
        self.check_for_code(status)
        return 

    def execute_generic_command(self, session_handle: int, resources: str, command_name: str, timeout: float) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        command_name_bytes = command_name.encode('utf-8')
        timeout_c = ctypes.c_double(timeout)
        status = lib.niSLSC_ExecuteGenericCommand(session_handle_c, resources_bytes, command_name_bytes, timeout_c)
        self.check_for_code(status)
        return 

    def read_register_uint8(self, session_handle: int, device_name: str, register_address: int) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint8()
        status = lib.niSLSC_ReadRegisterUInt8(session_handle_c, device_name_bytes, register_address_c, ctypes.byref(data_c))
        self.check_for_code(status)
        return data_c.value

    def read_register_uint16(self, session_handle: int, device_name: str, register_address: int) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint16()
        status = lib.niSLSC_ReadRegisterUInt16(session_handle_c, device_name_bytes, register_address_c, ctypes.byref(data_c))
        self.check_for_code(status)
        return data_c.value

    def read_register_uint32(self, session_handle: int, device_name: str, register_address: int) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint32()
        status = lib.niSLSC_ReadRegisterUInt32(session_handle_c, device_name_bytes, register_address_c, ctypes.byref(data_c))
        self.check_for_code(status)
        return data_c.value

    def read_register_uint64(self, session_handle: int, device_name: str, register_address: int) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint64()
        status = lib.niSLSC_ReadRegisterUInt64(session_handle_c, device_name_bytes, register_address_c, ctypes.byref(data_c))
        self.check_for_code(status)
        return data_c.value

    def write_register_uint8(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint8(data)
        status = lib.niSLSC_WriteRegisterUInt8(session_handle_c, device_name_bytes, register_address_c, data_c)
        self.check_for_code(status)
        return 

    def write_register_uint16(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint16(data)
        status = lib.niSLSC_WriteRegisterUInt16(session_handle_c, device_name_bytes, register_address_c, data_c)
        self.check_for_code(status)
        return 

    def write_register_uint32(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint32(data)
        status = lib.niSLSC_WriteRegisterUInt32(session_handle_c, device_name_bytes, register_address_c, data_c)
        self.check_for_code(status)
        return 

    def write_register_uint64(self, session_handle: int, device_name: str, register_address: int, data: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        register_address_c = ctypes.c_uint32(register_address)
        data_c = ctypes.c_uint64(data)
        status = lib.niSLSC_WriteRegisterUInt64(session_handle_c, device_name_bytes, register_address_c, data_c)
        self.check_for_code(status)
        return 

    def get_nvmem_bytes(self, session_handle: int, nvmem_area: str, nvmem_address: int, num_byte: int) -> bytes:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_bytes = nvmem_area.encode('utf-8')
        nvmem_address_c = ctypes.c_uint32(nvmem_address)
        byte_array = (ctypes.c_uint8 * num_byte)()
        status = lib.niSLSC_GetNVMEMBytes(session_handle_c, nvmem_area_bytes, nvmem_address_c, byte_array, num_byte)
        self.check_for_code(status)
        return bytes(byte_array)

    def set_nvmem_bytes(self, session_handle: int, nvmem_area: str, nvmem_address: int, bytes_data: bytes, serial_number: str, password: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_bytes = nvmem_area.encode('utf-8')
        nvmem_address_c = ctypes.c_uint32(nvmem_address)
        byte_array_size = len(bytes_data)
        byte_array = (ctypes.c_uint8 * byte_array_size)(*bytes_data)
        serial_number_bytes = serial_number.encode('utf-8')
        password_bytes = password.encode('utf-8')
        status = lib.niSLSC_SetNVMEMBytes(session_handle_c, nvmem_area_bytes, nvmem_address_c, byte_array, byte_array_size, serial_number_bytes, password_bytes)
        self.check_for_code(status)
        return 

    def commit_nvmem_areas(self, session_handle: int, nvmem_area_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        nvmem_area_names_bytes = nvmem_area_names.encode('utf-8')
        status = lib.niSLSC_CommitNVMEMAreas(session_handle_c, nvmem_area_names_bytes)
        self.check_for_code(status)
        return 

    def commit_nvmem_for_devices(self, session_handle: int, device_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        status = lib.niSLSC_CommitNVMEMForDevices(session_handle_c, device_names_bytes)
        self.check_for_code(status)
        return 

    def commit_nvmem_for_session(self, session_handle: int) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        status = lib.niSLSC_CommitNVMEMForSession(session_handle_c)
        self.check_for_code(status)
        return 

    def commit_nvmem_generic(self, session_handle: int, resources: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        resources_bytes = resources.encode('utf-8')
        status = lib.niSLSC_CommitNVMEMGeneric(session_handle_c, resources_bytes)
        self.check_for_code(status)
        return 

    def get_linear_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[float, float]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        slope_c = ctypes.c_double()
        intercept_c = ctypes.c_double()
        status = lib.niSLSC_GetLinearScalingParameters(session_handle_c, physical_channel_names_bytes, ctypes.byref(slope_c), ctypes.byref(intercept_c))
        self.check_for_code(status)
        return slope_c.value, intercept_c.value

    def get_polynomial_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[list[float], list[float]]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        forward_coefficient_actual_size = ctypes.c_size_t()
        reverse_coefficient_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPolynomialScalingParameters(session_handle_c, physical_channel_names_bytes, None, 0, ctypes.byref(forward_coefficient_actual_size), None, 0, ctypes.byref(reverse_coefficient_actual_size))
        if forward_coefficient_actual_size.value <= 0 or reverse_coefficient_actual_size.value <= 0:
            self.check_for_code(status)
        forward_coefficient_c = (ctypes.c_double * forward_coefficient_actual_size.value)()
        reverse_coefficient_c = (ctypes.c_double * reverse_coefficient_actual_size.value)()
        status = lib.niSLSC_GetPolynomialScalingParameters(session_handle_c, physical_channel_names_bytes, forward_coefficient_c, forward_coefficient_actual_size.value, None, reverse_coefficient_c, reverse_coefficient_actual_size.value, None)
        self.check_for_code(status)
        forward_coefficient_array = [forward_coefficient_c[i] for i in range(forward_coefficient_actual_size.value)]
        reverse_coefficient_array = [reverse_coefficient_c[i] for i in range(reverse_coefficient_actual_size.value)]
        return forward_coefficient_array, reverse_coefficient_array

    def get_table_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[list[float], list[float], int]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        scaled_value_actual_size = ctypes.c_size_t()
        prescale_value_actual_size = ctypes.c_size_t()
        coercion_c = ctypes.c_int32()
        status = lib.niSLSC_GetTableScalingParameters(session_handle_c, physical_channel_names_bytes, None, 0, ctypes.byref(scaled_value_actual_size), None, 0, ctypes.byref(prescale_value_actual_size))
        if scaled_value_actual_size.value <= 0 or prescale_value_actual_size.value <= 0:
            self.check_for_code(status)
        scaled_value_c = (ctypes.c_double * scaled_value_actual_size.value)()
        prescale_value_c = (ctypes.c_double * prescale_value_actual_size.value)()
        status = lib.niSLSC_GetTableScalingParameters(session_handle_c, physical_channel_names_bytes, scaled_value_c, scaled_value_actual_size.value, None, prescale_value_c, prescale_value_actual_size.value, None, ctypes.byref(coercion_c))
        self.check_for_code(status)
        scaled_value_array = [scaled_value_c[i] for i in range(scaled_value_actual_size.value)]
        prescale_value_array = [prescale_value_c[i] for i in range(prescale_value_actual_size.value)]
        return scaled_value_array, prescale_value_array, coercion_c.value

    def get_user_defined_scaling_parameters(self, session_handle: int, physical_channel_names: str) -> tuple[list[str], list[float]]:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        user_defined_parameter_names_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_user_defined_parameter_names = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        user_defined_parameter_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetUserDefinedScalingParameters(session_handle_c, physical_channel_names_bytes, ctypes.byref(user_defined_parameter_names_ptr), ctypes.byref(num_user_defined_parameter_names), None, 0, ctypes.byref(required_buffer_size), None, 0, ctypes.byref(user_defined_parameter_value_actual_size))
        if required_buffer_size.value <= 0 or user_defined_parameter_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        user_defined_parameter_value_c = (ctypes.c_double * user_defined_parameter_value_actual_size.value)()
        status = lib.niSLSC_GetUserDefinedScalingParameters(session_handle_c, physical_channel_names_bytes, ctypes.byref(user_defined_parameter_names_ptr), ctypes.byref(num_user_defined_parameter_names), buffer, required_buffer_size.value, None, user_defined_parameter_value_c, user_defined_parameter_value_actual_size.value, None)
        self.check_for_code(status)
        user_defined_parameter_names_array = []
        for i in range(num_user_defined_parameter_names.value):
            user_defined_parameter_names_array.append(ctypes.string_at(user_defined_parameter_names_ptr[i]).decode('utf-8'))
        user_defined_parameter_value_array = [user_defined_parameter_value_c[i] for i in range(user_defined_parameter_value_actual_size.value)]
        return user_defined_parameter_names_array, user_defined_parameter_value_array

    def get_user_defined_scaling_equation(self, session_handle: int, physical_channel_names: str) -> str:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        user_defined_equation_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetUserDefinedScalingEquation(session_handle_c, physical_channel_names_bytes, None, 0, ctypes.byref(user_defined_equation_actual_size))
        if user_defined_equation_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(user_defined_equation_actual_size.value)
        status = lib.niSLSC_GetUserDefinedScalingEquation(session_handle_c, physical_channel_names_bytes, buffer, user_defined_equation_actual_size.value, None)
        self.check_for_code(status)
        user_defined_equation_value = buffer.value.decode('utf-8')
        return user_defined_equation_value

    def set_linear_scaling_parameters(self, session_handle: int, physical_channel_names: str, slope: float, intercept: float, serial_number: str, password: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        slope_c = ctypes.c_double(slope)
        intercept_c = ctypes.c_double(intercept)
        serial_number_bytes = serial_number.encode('utf-8')
        password_bytes = password.encode('utf-8')
        status = lib.niSLSC_SetLinearScalingParameters(session_handle_c, physical_channel_names_bytes, slope_c, intercept_c, serial_number_bytes, password_bytes)
        self.check_for_code(status)
        return 

    def set_polynomial_scaling_parameters(self, session_handle: int, physical_channel_names: str, forward_coefficient: list[float], reverse_coefficient: list[float], serial_number: str, password: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        forward_coefficient_array = (ctypes.c_double * len(forward_coefficient))(*forward_coefficient)
        forward_coefficient_array_size = len(forward_coefficient)
        reverse_coefficient_array = (ctypes.c_double * len(reverse_coefficient))(*reverse_coefficient)
        reverse_coefficient_array_size = len(reverse_coefficient)
        serial_number_bytes = serial_number.encode('utf-8')
        password_bytes = password.encode('utf-8')
        status = lib.niSLSC_SetPolynomialScalingParameters(session_handle_c, physical_channel_names_bytes, forward_coefficient_array, forward_coefficient_array_size, reverse_coefficient_array, reverse_coefficient_array_size, serial_number_bytes, password_bytes)
        self.check_for_code(status)
        return 

    def set_table_scaling_parameters(self, session_handle: int, physical_channel_names: str, scaled_value: list[float], prescale_value: list[float], coercion: int, serial_number: str, password: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        scaled_value_array = (ctypes.c_double * len(scaled_value))(*scaled_value)
        scaled_value_array_size = len(scaled_value)
        prescale_value_array = (ctypes.c_double * len(prescale_value))(*prescale_value)
        prescale_value_array_size = len(prescale_value)
        coercion_c = ctypes.c_int32(coercion)
        serial_number_bytes = serial_number.encode('utf-8')
        password_bytes = password.encode('utf-8')
        status = lib.niSLSC_SetTableScalingParameters(session_handle_c, physical_channel_names_bytes, scaled_value_array, scaled_value_array_size, prescale_value_array, prescale_value_array_size, coercion_c, serial_number_bytes, password_bytes)
        self.check_for_code(status)
        return 

    def set_user_defined_scaling_parameters(self, session_handle: int, physical_channel_names: str, user_defined_parameter_name: list[str], user_defined_parameter_value: list[float], serial_number: str, password: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        user_defined_parameter_name_bytes = [string.encode('utf-8') for string in user_defined_parameter_name]
        array_type = ctypes.c_char_p * len(user_defined_parameter_name_bytes)
        user_defined_parameter_name_array = array_type(*user_defined_parameter_name_bytes)
        user_defined_parameter_value_array = (ctypes.c_double * len(user_defined_parameter_value))(*user_defined_parameter_value)
        user_defined_parameter_value_array_size = len(user_defined_parameter_value)
        serial_number_bytes = serial_number.encode('utf-8')
        password_bytes = password.encode('utf-8')
        status = lib.niSLSC_SetUserDefinedScalingParameters(session_handle_c, physical_channel_names_bytes, user_defined_parameter_name_array, ctypes.c_size_t(len(user_defined_parameter_name_bytes)), user_defined_parameter_value_array, user_defined_parameter_value_array_size, serial_number_bytes, password_bytes)
        self.check_for_code(status)
        return 

    def set_user_defined_scaling_equation(self, session_handle: int, physical_channel_names: str, user_defined_equation: str, serial_number: str, password: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        user_defined_equation_bytes = user_defined_equation.encode('utf-8')
        serial_number_bytes = serial_number.encode('utf-8')
        password_bytes = password.encode('utf-8')
        status = lib.niSLSC_SetUserDefinedScalingEquation(session_handle_c, physical_channel_names_bytes, user_defined_equation_bytes, serial_number_bytes, password_bytes)
        self.check_for_code(status)
        return 

    def commit_scaling_for_devices(self, session_handle: int, device_names: str) -> None:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_names_bytes = device_names.encode('utf-8')
        status = lib.niSLSC_CommitScalingForDevices(session_handle_c, device_names_bytes)
        self.check_for_code(status)
        return 

    def open_device_command(self, session_handle: int, device_name: str, command_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        command_name_bytes = command_name.encode('utf-8')
        command_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenDeviceCommand(session_handle_c, device_name_bytes, command_name_bytes, ctypes.byref(command_handle_c))
        self.check_for_code(status)
        return command_handle_c.value or 0

    def open_physical_channel_command(self, session_handle: int, physical_channel_names: str, command_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        command_name_bytes = command_name.encode('utf-8')
        command_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenPhysicalChannelCommand(session_handle_c, physical_channel_names_bytes, command_name_bytes, ctypes.byref(command_handle_c))
        self.check_for_code(status)
        return command_handle_c.value or 0

    def open_generic_command(self, session_handle: int, resource: str, command_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        resource_bytes = resource.encode('utf-8')
        command_name_bytes = command_name.encode('utf-8')
        command_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenGenericCommand(session_handle_c, resource_bytes, command_name_bytes, ctypes.byref(command_handle_c))
        self.check_for_code(status)
        return command_handle_c.value or 0

    def close_command(self, command_handle: int) -> None:
        command_handle_c = ctypes.c_void_p(command_handle)
        status = lib.niSLSC_CloseCommand(command_handle_c)
        self.check_for_code(status)
        return 

    def get_command_property_string(self, command_handle: int, property_name: str) -> str:
        command_handle_c = ctypes.c_void_p(command_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetCommandPropertyString(command_handle_c, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetCommandPropertyString(command_handle_c, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def open_device_property(self, session_handle: int, device_name: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        device_name_bytes = device_name.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenDeviceProperty(session_handle_c, device_name_bytes, property_name_bytes, ctypes.byref(property_handle_c))
        self.check_for_code(status)
        return property_handle_c.value or 0

    def open_physical_channel_property(self, session_handle: int, physical_channel_names: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        physical_channel_names_bytes = physical_channel_names.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenPhysicalChannelProperty(session_handle_c, physical_channel_names_bytes, property_name_bytes, ctypes.byref(property_handle_c))
        self.check_for_code(status)
        return property_handle_c.value or 0

    def open_driver_defined_property(self, session_handle: int, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenDriverDefinedProperty(session_handle_c, property_name_bytes, ctypes.byref(property_handle_c))
        self.check_for_code(status)
        return property_handle_c.value or 0

    def open_generic_property(self, session_handle: int, resource: str, property_name: str) -> int:
        session_handle_c = ctypes.c_void_p(session_handle)
        resource_bytes = resource.encode('utf-8')
        property_name_bytes = property_name.encode('utf-8')
        property_handle_c = ctypes.c_void_p()
        status = lib.niSLSC_OpenGenericProperty(session_handle_c, resource_bytes, property_name_bytes, ctypes.byref(property_handle_c))
        self.check_for_code(status)
        return property_handle_c.value or 0

    def close_property(self, property_handle: int) -> None:
        property_handle_c = ctypes.c_void_p(property_handle)
        status = lib.niSLSC_CloseProperty(property_handle_c)
        self.check_for_code(status)
        return 

    def get_property_property_bool(self, property_handle: int, property_name: str) -> bool:
        property_handle_c = ctypes.c_void_p(property_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_bool()
        status = lib.niSLSC_GetPropertyPropertyBool(property_handle_c, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_property_property_int32(self, property_handle: int, property_name: str) -> int:
        property_handle_c = ctypes.c_void_p(property_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_c = ctypes.c_int32()
        status = lib.niSLSC_GetPropertyPropertyInt32(property_handle_c, property_name_bytes, ctypes.byref(property_value_c))
        self.check_for_code(status)
        return property_value_c.value

    def get_property_property_int32_array(self, property_handle: int, property_name: str) -> list[int]:
        property_handle_c = ctypes.c_void_p(property_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPropertyPropertyInt32Array(property_handle_c, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        property_value_c = (ctypes.c_int32 * property_value_actual_size.value)()
        status = lib.niSLSC_GetPropertyPropertyInt32Array(property_handle_c, property_name_bytes, property_value_c, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_array = [property_value_c[i] for i in range(property_value_actual_size.value)]
        return property_value_array

    def get_property_property_string(self, property_handle: int, property_name: str) -> str:
        property_handle_c = ctypes.c_void_p(property_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_actual_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPropertyPropertyString(property_handle_c, property_name_bytes, None, 0, ctypes.byref(property_value_actual_size))
        if property_value_actual_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(property_value_actual_size.value)
        status = lib.niSLSC_GetPropertyPropertyString(property_handle_c, property_name_bytes, buffer, property_value_actual_size.value, None)
        self.check_for_code(status)
        property_value_value = buffer.value.decode('utf-8')
        return property_value_value

    def get_property_property_string_array(self, property_handle: int, property_name: str) -> list[str]:
        property_handle_c = ctypes.c_void_p(property_handle)
        property_name_bytes = property_name.encode('utf-8')
        property_value_ptr = ctypes.POINTER(ctypes.c_char_p)()
        num_property_value = ctypes.c_size_t()
        required_buffer_size = ctypes.c_size_t()
        status = lib.niSLSC_GetPropertyPropertyStringArray(property_handle_c, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), None, 0, ctypes.byref(required_buffer_size))
        if required_buffer_size.value <= 0:
            self.check_for_code(status)
        buffer = ctypes.create_string_buffer(required_buffer_size.value)
        status = lib.niSLSC_GetPropertyPropertyStringArray(property_handle_c, property_name_bytes, ctypes.byref(property_value_ptr), ctypes.byref(num_property_value), buffer, required_buffer_size.value, None)
        self.check_for_code(status)
        property_value_array = []
        for i in range(num_property_value.value):
            property_value_array.append(ctypes.string_at(property_value_ptr[i]).decode('utf-8'))
        return property_value_array

    def check_for_code(self, error_code: int) -> None:
        if error_code != 0:
            if error_code < 0:
                raise SLSCError("", error_code)
            elif error_code > 0:
                warnings.warn(SLSCWarning("", error_code))

