from __future__ import annotations

import fnmatch
import json
from typing import Any

DEFAULT_SECURITY_HEADERS = {
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
}

SENSITIVE_VALUE_PATTERNS = (
    "*password*",
    "*secret*",
    "*token*",
    "*api_key*",
    "*apikey*",
    "*authorization*",
)


def get_response_headers(response_or_headers: Any) -> dict[str, str]:
    headers = response_or_headers.headers if hasattr(response_or_headers, "headers") else response_or_headers
    return {str(key).lower(): str(value) for key, value in dict(headers).items()}


def assert_header_present(response_or_headers: Any, header_name: str) -> None:
    headers = get_response_headers(response_or_headers)
    assert header_name.lower() in headers, f"Expected response header {header_name!r} to exist."


def assert_security_headers(
    response_or_headers: Any,
    required_headers: set[str] | None = None,
) -> None:
    headers = get_response_headers(response_or_headers)
    required = {header.lower() for header in (required_headers or DEFAULT_SECURITY_HEADERS)}
    missing = sorted(required - set(headers))
    assert not missing, f"Missing expected security headers: {missing!r}"


def assert_no_sensitive_values_in_text(
    text: str,
    patterns: tuple[str, ...] = SENSITIVE_VALUE_PATTERNS,
) -> None:
    lowered_text = text.lower()
    matches = [pattern for pattern in patterns if fnmatch.fnmatch(lowered_text, pattern)]
    assert not matches, f"Sensitive value patterns found in text: {matches!r}"


def assert_no_sensitive_values_in_json(
    payload: Any,
    patterns: tuple[str, ...] = SENSITIVE_VALUE_PATTERNS,
) -> None:
    serialized = json.dumps(payload, default=str).lower()
    matches = [pattern for pattern in patterns if fnmatch.fnmatch(serialized, pattern)]
    assert not matches, f"Sensitive value patterns found in JSON payload: {matches!r}"
