from __future__ import annotations

from unittest.mock import Mock


def expect_initialize_library(interpreter: Mock, library_handle: int = 1) -> None:
    """Expect a call to interpreter.initialize_library."""
    interpreter.initialize_library.return_value = library_handle


def expect_initialize_session_with_devices(
    interpreter: Mock, session_handle: int = 100
) -> None:
    """Expect a call to interpreter.initialize_session_with_devices."""
    interpreter.initialize_session_with_devices.return_value = session_handle


def expect_initialize_session_with_nvmem_areas(
    interpreter: Mock, session_handle: int = 200
) -> None:
    """Expect a call to interpreter.initialize_session_with_nvmem_areas."""
    interpreter.initialize_session_with_nvmem_areas.return_value = session_handle


def expect_initialize_session_with_physical_channels(
    interpreter: Mock, session_handle: int = 300
) -> None:
    """Expect a call to interpreter.initialize_session_with_physical_channels."""
    interpreter.initialize_session_with_physical_channels.return_value = session_handle


def expect_initialize_session_without_resources(
    interpreter: Mock, session_handle: int = 400
) -> None:
    """Expect a call to interpreter.initialize_session_without_resources."""
    interpreter.initialize_session_without_resources.return_value = session_handle