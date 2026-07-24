from __future__ import annotations

from unittest.mock import Mock

from nislsc import Library
from nislsc.constants import Language
from tests.unit._session_utils import expect_initialize_library


def test___init___initialize_library_called_with_version(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 42)

    with Library() as lib:
        interpreter.initialize_library.assert_called_once_with(1)
        assert lib._interpreter._library_handle == 42


def test___init___language_is_current_thread_locale(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)

    with Library() as lib:
        assert lib.language == Language.CURRENT_THREAD_LOCALE


def test___language_provided___init___language_set_on_interpreter(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)

    with Library(Language.ENGLISH) as lib:
        assert lib.language == Language.ENGLISH
        assert lib._interpreter._language == Language.ENGLISH


def test___library_opened___close___finalize_library_called_with_handle(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 42)
    lib = Library()

    lib.close()

    interpreter.finalize_library.assert_called_once_with(42)
    assert lib._interpreter._library_handle == 0


def test___library_opened___close_twice___close___finalize_library_called_once(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 42)
    lib = Library()

    lib.close()
    lib.close()

    interpreter.finalize_library.assert_called_once_with(42)


def test___context_manager___close___finalize_library_called_on_exit(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 42)

    with Library():
        interpreter.finalize_library.assert_not_called()

    interpreter.finalize_library.assert_called_once_with(42)


def test___library_opened___set_language___updates_interpreter_language(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter)

    with Library() as lib:
        lib.language = Language.JAPANESE

        assert lib.language == Language.JAPANESE
        assert lib._interpreter._language == Language.JAPANESE


def test___library_opened___get_error_description___delegates_to_interpreter(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 1)
    interpreter.get_error_description.return_value = "Device not found."

    with Library() as lib:
        result = lib.get_error_description(-250806)

    interpreter.get_error_description.assert_called_once()
    assert result == "Device not found."


def test___language_provided___get_error_description___passes_language_to_interpreter(
    interpreter: Mock,
) -> None:
    expect_initialize_library(interpreter, 1)
    interpreter.get_error_description.return_value = "Erreur."

    with Library() as lib:
        result = lib.get_error_description(-250806, Language.FRENCH)

    call_args = interpreter.get_error_description.call_args
    assert call_args.args[2] == Language.FRENCH
    assert result == "Erreur."
