from generated.nislsc._library_interpreter import LibraryInterpreter
from handwritten.error import SLSCError, SLSCWarning

class NISLSC(BaseInterpreter):
    def __init__(self, version: int = 0x1950270f):
        self.interpreter = LibraryInterpreter()
        self.handle = self.lib.initialize_library(version)

    def __del__(self):
      self.lib.finalize_library(self.handle)

    def initialize_session_with_devices(
        self, library_handle:int, device_names: str, connection_timeout: int, reservation_access: int, reservation_group: str, reservation_timeout: int
    ) -> int:
        return self.lib.initialize_session_with_devices(
            self.handle, device_name, connection_timeout, reservation_access, reservation_group, reservation_timeout
        )


    niSLSC_InitializeSessionWithDevices

    niSLSC_InitializeSessionWithNVMEMAreas

    niSLSC_InitializeSessionWithPhysicalChannels

    niSLSC_InitializeSessionWithoutResources

    niSLSC_GetExtendedErrorInfo

    niSLSC_GetErrorDescription