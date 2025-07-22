<%!
from utilities.function_helpers import get_function_parameter_list, get_function_return_type, is_creating_handle, is_defining_language, is_class_func
from utilities.interpreter_helpers import get_python_function_name, is_capi, is_param_input, is_param_output
from utilities.docstrings_helpers import generate_docstrings
%>\
from typing_extensions import Self

from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language
from nislsc.session._session import Session
from nislsc.utils import _select_interpreter, get_library_version
from types import TracebackType

class Library():
    """
    Represent Library class for NI SLSC.
    """
    def __init__(self, language: Language = Language.CURRENT_THREAD_LOCALE) -> None:
        """Create a library instance that handles session.

        Args:
            language (Language): The language to use for error messages and
                outputs.
        """
        self._interpreter = _select_interpreter()
        self._library_handle = self.initialize_library(get_library_version())
        self._language = language

    def __enter__(self) -> Self:
        """Enter the runtime context related to this object.

        Returns:
            Self: The library object itself.
        """
        return self
  
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        """Exit the runtime context and finalize the Library instance.

        Args:
            type: The exception type, if an exception was raised, otherwise 
                None.
            value: The exception value, if an exception was raised, otherwise
                None.
            traceback: The traceback, if an exception was raised, otherwise 
                None.
        """
        self.close()

    def __del__(self) -> None:
        """
        Remind the user that the Library instance is not finalized.
        """
        if self._library_handle is not None:
            warnings.warn(
                'Library was not finalized before it was destructed. Resources on the'
                'Library may still be reserved.',
                SLSCResourceWarning
            )

    @property
    def language(self) -> Language:
        """Get the current language setting.

        Returns:
            Language: An enum representing the current language.
        """
        return self._language

    @language.setter
    def language(self, language: Language) -> None:
        """Set the language for error messages and other outputs.

        Args:
            language: The language to set.
        """
        self._language = language

    def close(self) -> None:
        """
        Close the Library instance.
        """
        if self._library_handle is not None:
            self._interpreter.finalize_library(self._library_handle)
            self._library_handle = None

% for function in functions:
% if 'capi' in function['targets']:
% if is_class_func(function, "Library") and function["name"] != "FinalizeLibrary":
    def ${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", True, True)])})${get_function_return_type(function)}:
% for docstrings in generate_docstrings(function, "Library"):
        ${docstrings}
% endfor
% if is_defining_language(function):
        language = self._language if language == Language.UNDEFINED else language
% endif
        return self._interpreter.${get_python_function_name(function)}(${", ".join([param for param in get_function_parameter_list(function, "Library", False)])})

% endif
% endif
% endfor