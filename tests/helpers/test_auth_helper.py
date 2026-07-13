import base64

import pytest

from utils.helpers.auth import ApiKeyAuth, BasicAuth, BearerTokenAuth, NoAuth, redact_headers

pytestmark = [pytest.mark.helpers, pytest.mark.auth]


def test_bearer_token_auth_builds_authorization_header():
    auth = BearerTokenAuth("token-123")

    assert auth.headers() == {"Authorization": "Bearer token-123"}
    assert auth.params() == {}


def test_basic_auth_builds_encoded_header():
    auth = BasicAuth("user", "pass")
    expected = base64.b64encode(b"user:pass").decode("ascii")

    assert auth.headers()["Authorization"] == f"Basic {expected}"


def test_api_key_auth_supports_header_and_query_locations():
    assert ApiKeyAuth("X-API-Key", "secret").headers() == {"X-API-Key": "secret"}
    assert ApiKeyAuth("api_key", "secret", location="query").params() == {"api_key": "secret"}


def test_no_auth_is_empty():
    auth = NoAuth()

    assert auth.headers() == {}
    assert auth.params() == {}


def test_redact_headers_masks_sensitive_values():
    redacted = redact_headers({"Authorization": "Bearer secret", "X-Trace-ID": "abc"})

    assert redacted["Authorization"] == "***"
    assert redacted["X-Trace-ID"] == "abc"
