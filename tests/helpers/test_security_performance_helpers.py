from datetime import timedelta

import httpx
import pytest

from utils.helpers.performance import assert_response_time_under, summarize_response_timings
from utils.helpers.security import (
    assert_header_present,
    assert_no_sensitive_values_in_json,
    assert_no_sensitive_values_in_text,
    assert_security_headers,
    get_response_headers,
)

pytestmark = [pytest.mark.helpers, pytest.mark.security, pytest.mark.performance]


def test_security_headers_and_sensitive_value_helpers():
    response = httpx.Response(
        200,
        headers={
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
        },
        json={"message": "ok"},
    )

    assert get_response_headers(response)["x-frame-options"] == "DENY"
    assert_header_present(response, "x-content-type-options")
    assert_security_headers(response)
    assert_no_sensitive_values_in_text("normal response body")
    assert_no_sensitive_values_in_json({"message": "normal response body"})

    with pytest.raises(AssertionError, match="Sensitive value patterns"):
        assert_no_sensitive_values_in_text("api_token=abc123")


def test_performance_helpers_summarize_response_timings():
    response = httpx.Response(200)
    response._elapsed = timedelta(milliseconds=25)

    assert assert_response_time_under(response, 100) == 25
    assert summarize_response_timings([response])["avg_ms"] == 25
