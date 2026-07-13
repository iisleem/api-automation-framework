import httpx
import pytest

from clients import ApiClient
from utils.helpers.assertions import assert_json_path, assert_status

pytestmark = [pytest.mark.negative, pytest.mark.auth, pytest.mark.rest]


def test_missing_token_returns_unauthorized_error():
    client = ApiClient("https://mock.api.local", transport=httpx.MockTransport(_auth_handler))

    response = client.get("/secure/profile")

    assert_status(response, 401)
    assert_json_path(response.json(), "error.code", "unauthorized")
    client.close()


def _auth_handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/secure/profile" and "authorization" not in request.headers:
        return httpx.Response(401, json={"error": {"code": "unauthorized", "message": "Missing token"}})
    return httpx.Response(200, json={"id": 1})
