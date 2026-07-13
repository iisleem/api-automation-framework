"""Focused API assertion helpers."""

from __future__ import annotations

import re
from typing import Any

import httpx

_PATH_TOKEN = re.compile(r"([A-Za-z0-9_-]+)|\[(\d+)]")


def assert_status(response: httpx.Response, expected_status: int | list[int] | tuple[int, ...]) -> None:
    expected = [expected_status] if isinstance(expected_status, int) else list(expected_status)
    assert response.status_code in expected, (
        f"Expected status {expected}, got {response.status_code}. Response body: {response.text[:500]}"
    )


def assert_header(response: httpx.Response, name: str, expected_value: str | None = None) -> None:
    assert name in response.headers, f"Expected header '{name}' to exist"
    if expected_value is not None:
        assert response.headers[name] == expected_value, (
            f"Expected header '{name}' to equal '{expected_value}', got '{response.headers[name]}'"
        )


def get_by_path(payload: Any, path: str) -> Any:
    current = payload
    for key, index in _PATH_TOKEN.findall(path):
        if key:
            if not isinstance(current, dict):
                raise KeyError(f"Cannot read key '{key}' from non-object at '{path}'")
            current = current[key]
        else:
            if not isinstance(current, list):
                raise IndexError(f"Cannot read index {index} from non-list at '{path}'")
            current = current[int(index)]
    return current


def assert_json_path(payload: dict[str, Any], path: str, expected_value: Any = None) -> Any:
    actual = get_by_path(payload, path)
    if expected_value is not None:
        assert actual == expected_value, f"Expected JSON path '{path}' to be {expected_value!r}, got {actual!r}"
    return actual


def assert_response_time_under(response: httpx.Response, max_ms: float) -> None:
    try:
        elapsed_ms = response.elapsed.total_seconds() * 1000
    except RuntimeError as exc:
        raise AssertionError("Response elapsed time is unavailable on this response object") from exc
    assert elapsed_ms <= max_ms, f"Expected response time <= {max_ms}ms, got {elapsed_ms:.2f}ms"
