import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from clients import ApiClient
from services import BookingService
from utils.helpers.assertions import assert_header, assert_json_path, assert_status
from utils.helpers.data import booking_payload as build_booking_payload

pytestmark = [pytest.mark.examples, pytest.mark.rest]


def test_mock_booking_api_example(schema_validator):
    transport = httpx.MockTransport(_build_booking_handler())

    with ApiClient("https://mock.api.local", transport=transport) as client:
        service = BookingService(client)

        create_response = service.create_booking(build_booking_payload("Example", "Guest"))
        _assert_booking_response(create_response, schema_validator, expected_status=201, expected_firstname="Example")

        booking_id = assert_json_path(create_response.json(), "bookingid", 101)
        fetch_response = service.get_booking(booking_id)
        _assert_booking_response(fetch_response, schema_validator, expected_status=200, expected_firstname="Example")


def _assert_booking_response(response, schema_validator, *, expected_status: int, expected_firstname: str) -> None:
    assert_status(response, expected_status)
    assert_header(response, "content-type", "application/json")
    assert_json_path(response.json(), "booking.firstname", expected_firstname)
    schema_validator.assert_matches_schema(response.json(), "schemas/rest/booking.schema.json")


def _build_booking_handler() -> Callable[[httpx.Request], httpx.Response]:
    bookings: dict[int, dict[str, Any]] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/bookings":
            payload = json.loads(request.content.decode("utf-8"))
            booking_id = 101
            bookings[booking_id] = payload
            return httpx.Response(
                201,
                json={"bookingid": booking_id, "booking": payload},
                headers={"content-type": "application/json"},
            )

        if request.method == "GET" and request.url.path.startswith("/bookings/"):
            booking_id = int(request.url.path.rsplit("/", 1)[-1])
            booking = bookings.get(booking_id)
            if booking is None:
                return httpx.Response(404, json={"error": "booking not found"})
            return httpx.Response(
                200,
                json={"bookingid": booking_id, "booking": booking},
                headers={"content-type": "application/json"},
            )

        return httpx.Response(404, json={"error": "not found"})

    return handler
