from datetime import timedelta

import httpx
import pytest

from utils.helpers.assertions import (
    assert_header,
    assert_json_path,
    assert_response_time_under,
    assert_status,
    get_by_path,
)

pytestmark = pytest.mark.regression


def test_api_assertions_cover_status_headers_json_paths_and_timing():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"X-Trace-ID": "trace-1"},
            json={"data": {"users": [{"id": 123, "name": "Ismail"}]}},
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        response = client.get("https://mock.api.local/users")
    response._elapsed = timedelta(milliseconds=25)

    assert_status(response, 200)
    assert_header(response, "X-Trace-ID", "trace-1")
    assert_json_path(response.json(), "data.users[0].id", 123)
    assert get_by_path(response.json(), "data.users[0].name") == "Ismail"
    assert_response_time_under(response, 1000)
