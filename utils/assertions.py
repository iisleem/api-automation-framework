from __future__ import annotations

from typing import Any


def assert_equal(actual: Any, expected: Any, message: str = "") -> None:
    assert actual == expected, message or f"Expected {expected!r}, got {actual!r}"


def assert_true(condition: bool, message: str = "") -> None:
    assert condition, message or "Expected condition to be truthy"


def assert_contains(container: Any, member: Any, message: str = "") -> None:
    assert member in container, message or f"Expected {member!r} to exist in {container!r}"
