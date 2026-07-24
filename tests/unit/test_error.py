from __future__ import annotations

import warnings

import pytest

from nislsc.error import SLSCError, SLSCResourceWarning, SLSCWarning
from nislsc.error_codes import SLSCErrors, SLSCWarnings


def test___slscerror___known_error_code___error_code_stored() -> None:
    err = SLSCError("Device not found.", -250806)

    assert err.error_code == -250806


def test___slscerror___error_code_as_string___coerced_to_int() -> None:
    err = SLSCError("Some error.", "-250806")  # type: ignore[arg-type]

    assert err.error_code == -250806
    assert isinstance(err.error_code, int)


def test___slscerror___known_error_code___error_type_matches_enum() -> None:
    err = SLSCError("Device not found.", -250806)

    assert err.error_type == SLSCErrors.DEVICE_NOT_FOUND


def test___slscerror___unknown_error_code___error_type_is_unknown() -> None:
    err = SLSCError("Unexpected error.", -999999)

    assert err.error_type == SLSCErrors.UNKNOWN


def test___slscerror___internal_error_code___error_type_matches_enum() -> None:
    err = SLSCError("Internal error.", -250800)

    assert err.error_type == SLSCErrors.INTERNAL


def test___slscerror___message_with_status_code___message_not_duplicated() -> None:
    err = SLSCError("Device not found.\n\nStatus Code: -250806", -250806)

    assert str(err).count("-250806") == 1


def test___slscerror___message_without_status_code___status_code_appended() -> None:
    err = SLSCError("Device not found.", -250806)

    assert "-250806" in str(err)


def test___slscerror___empty_message___default_message_with_status_code() -> None:
    err = SLSCError("", -250806)

    assert "Description could not be found" in str(err)
    assert "-250806" in str(err)


def test___slscerror___whitespace_only_message___default_message_with_status_code() -> None:
    err = SLSCError("   ", -250806)

    assert "Description could not be found" in str(err)
    assert "-250806" in str(err)


def test___slscerror___none_message___default_message_with_status_code() -> None:
    err = SLSCError(None, -250806)  # type: ignore[arg-type]

    assert "Description could not be found" in str(err)
    assert "-250806" in str(err)


def test___slscerror___raised_and_caught_as_slscerror___succeeds() -> None:
    with pytest.raises(SLSCError):
        raise SLSCError("Device not found.", -250806)


def test___slscerror___raised_and_caught_as_exception___succeeds() -> None:
    with pytest.raises(Exception):
        raise SLSCError("Device not found.", -250806)


def test___slscwarning___known_warning_code___error_code_stored() -> None:
    w = SLSCWarning("Scaling timestamp outdated.", 250800)

    assert w.error_code == 250800


def test___slscwarning___error_code_as_string___coerced_to_int() -> None:
    w = SLSCWarning("Scaling timestamp outdated.", "250800")

    assert w.error_code == 250800
    assert isinstance(w.error_code, int)


def test___slscwarning___known_warning_code___error_type_matches_enum() -> None:
    w = SLSCWarning("Scaling timestamp outdated.", 250800)

    assert w.error_type == SLSCWarnings.SCALING_TIMESTAMP_OUTDATED


def test___slscwarning___unknown_warning_code___error_type_is_unknown() -> None:
    w = SLSCWarning("Some unknown warning.", 999999)

    assert w.error_type == SLSCWarnings.UNKNOWN


def test___slscwarning___message___includes_warning_code() -> None:
    w = SLSCWarning("Scaling timestamp outdated.", 250800)

    assert "250800" in str(w)


def test___slscwarning___message___includes_original_message() -> None:
    w = SLSCWarning("Scaling timestamp outdated.", 250800)

    assert "Scaling timestamp outdated." in str(w)


def test___slscwarning___message___formatted_with_warning_prefix() -> None:
    w = SLSCWarning("Scaling timestamp outdated.", 250800)

    assert str(w).startswith("\nWarning 250800 occurred.")


def test___slscwarning___emitted_via_warnings_warn___caught_by_pytest_warns() -> None:
    with pytest.warns(SLSCWarning):
        warnings.warn(SLSCWarning("Scaling timestamp outdated.", 250800))


def test___slscwarning___emitted___error_code_accessible_on_caught_warning() -> None:
    with pytest.warns(SLSCWarning) as warning_info:
        warnings.warn(SLSCWarning("Scaling timestamp outdated.", 250800))

    assert warning_info[0].message.error_code == 250800


def test___slscwarning___emitted___error_type_accessible_on_caught_warning() -> None:
    with pytest.warns(SLSCWarning) as warning_info:
        warnings.warn(SLSCWarning("Scaling timestamp outdated.", 250800))

    assert warning_info[0].message.error_type == SLSCWarnings.SCALING_TIMESTAMP_OUTDATED


def test___slscresourcewarning___is_subclass_of_resource_warning() -> None:
    assert issubclass(SLSCResourceWarning, ResourceWarning)


def test___slscresourcewarning___emitted___caught_by_pytest_warns() -> None:
    with pytest.warns(SLSCResourceWarning):
        warnings.warn("Resource was not released.", SLSCResourceWarning)
