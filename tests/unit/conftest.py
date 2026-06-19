from __future__ import annotations

from collections.abc import Generator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from nislsc import Library, Session
from nislsc._base_interpreter import BaseInterpreter
from nislsc.constants import Language, ReservationAccess
from tests.unit._session_utils import (
    expect_initialize_library,
    expect_initialize_session_with_devices,
)


@pytest.fixture
def interpreter(mocker: MockerFixture) -> Mock:
    """Create a mock interpreter.

    Patches _select_interpreter in all modules that call it, and patches
    get_library_version so Library.__init__ does not need a real driver.
    """
    mock_interpreter = mocker.create_autospec(BaseInterpreter)
    mock_interpreter._library_handle = 0
    mock_interpreter._language = Language.CURRENT_THREAD_LOCALE

    for target in (
        "nislsc.library._select_interpreter",
        "nislsc.utils._select_interpreter",
    ):
        stub = mocker.patch(target, autospec=True)
        stub.return_value = mock_interpreter

    mocker.patch("nislsc.library.get_library_version", return_value=1)

    return mock_interpreter


@pytest.fixture
def library(interpreter: Mock) -> Generator[Library, None, None]:
    """Create a Library instance backed by the mock interpreter."""
    expect_initialize_library(interpreter)
    with Library() as lib:
        yield lib


@pytest.fixture
def session(library: Library, interpreter: Mock) -> Generator[Session, None, None]:
    """Create a Session with devices, backed by the mock interpreter.

    This fixture owns the session.  Do not use it in tests that destroy the
    session, or you may get double-close warnings.
    """
    expect_initialize_session_with_devices(interpreter)
    with Session.initialize_session_with_devices(
        library, "Dev1", -1.0, ReservationAccess.NONE, "", -1.0
    ) as sess:
        yield sess