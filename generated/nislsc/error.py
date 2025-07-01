from nislsc.error_codes import SLSCErrors, SLSCWarnings

__all__ = ['SLSCError', 'SLSCWarning']

class Error(Exception):
    pass

class SLSCError(Error):
    def __init__(self, message: str, error_code: int) -> None:
        self._error_code = int(error_code)

        try:
            self._error_type = SLSCErrors(self._error_code)
        except ValueError:
            self._error_type = SLSCErrors.ERROR_UNKNOWN

        if not message:
            message = f'Description could not be found for the status code.\n\nStatus Code: {self._error_code}'

        super().__init__(message)

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_type(self) -> SLSCErrors:
        return self._error_type

class SLSCWarning(Warning):
    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(
            f'\nWarning {error_code} occurred.\n\n{message}')

        self._error_code = int(error_code)

        try:
            self._error_type = SLSCWarnings(self._error_code)
        except ValueError:
            self._error_type = SLSCWarnings.WARNING_UNKNOWN

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_type(self) -> SLSCWarnings:
        return self._error_type
