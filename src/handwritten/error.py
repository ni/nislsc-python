import warnings

from nislsc.error_codes import SLSCError

__all__ = ['SLSCError', 'SLSCWarning']

class Error(Exception):
    pass

class SLSCError(Error):
    def __init__(self, message, error_code):
        self._error_code = int(error_code)

        if not message:
            message = f'Description could not be found for the status code.\n\nStatus Code: {self._error_code}'

        super().__init__(message)

    @property
    def error_code(self):
        return self._error_code

    @property
    def error_code(self):
        return self._error_code


class SLSCWarning(Warning):
    def __init__(self, message, error_code):
        super().__init__(
            f'\nWarning {error_code} occurred.\n\n{message}')

        self._error_code = int(error_code)

    @property
    def error_code(self):
        return self._error_code