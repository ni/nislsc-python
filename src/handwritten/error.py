"""Handle SLSC exceptions and warnings.

This module provides custom exception and warning classes for handling
SLSC API errors and warnings.
"""

import warnings

from nislsc.error_codes import SLSCErrors, SLSCWarnings

__all__ = ["SLSCError", "SLSCWarning", "SLSCResourceWarning"]


class SLSCResourceWarning(ResourceWarning):
    """Warn about SLSC resource management issues."""

    pass


class Error(Exception):
    """Represent base exceptions for SLSC operations."""

    pass


class SLSCError(Error):
    """Handle NI-SLSC method errors."""

    def __init__(self, message: str, error_code: int) -> None:
        self._error_code = int(error_code)

        try:
            self._error_type = SLSCErrors(self._error_code)
        except ValueError:
            self._error_type = SLSCErrors.UNKNOWN

        if not message:
            message = f"Description could not be found for the status code.\n\nStatus Code: {self._error_code}"

        super().__init__(message)

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_type(self) -> SLSCErrors:
        return self._error_type


class SLSCWarning(Warning):
    """Warn about NI-SLSC method issues."""

    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(
            f'\nWarning {error_code} occurred.\n\n{message}')

        self._error_code = int(error_code)

        try:
            self._error_type = SLSCWarnings(self._error_code)
        except ValueError:
            self._error_type = SLSCWarnings.UNKNOWN

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_type(self) -> SLSCWarnings:
        return self._error_type
