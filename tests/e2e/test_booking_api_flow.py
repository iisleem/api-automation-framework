import json

import httpx
import pytest

from clients import ApiClient
from services import BookingService

pytestmark = [pytest.mark.e2e, pytest.mark.rest]


def test_create_and_read_booking_api_flow(schema_validator, booking_payload):
    client = ApiClient("https://mock.api.local", transport=httpx.MockTransport(_booking_flow_handler))
    service = BookingService(client)

    created = service.create_booking(booking_payload)
    booking_id = created.json()["bookingid"]
    fetched = service.get_booking(booking_id)

    assert fetched.json()["bookingid"] == booking_id
    schema_validator.assert_matches_schema(created.json(), "schemas/rest/booking.schema.json")
    schema_validator.assert_matches_schema(fetched.json(), "schemas/rest/booking.schema.json")
    client.close()


def _booking_flow_handler(request: httpx.Request) -> httpx.Response:
    if request.method == "POST" and request.url.path == "/bookings":
        payload = json.loads(request.content.decode("utf-8"))
        return httpx.Response(201, json={"bookingid": 501, "booking": payload})

    if request.method == "GET" and request.url.path == "/bookings/501":
        return httpx.Response(
            200,
            json={
                "bookingid": 501,
                "booking": {
                    "firstname": "Ismail",
                    "lastname": "Automation",
                    "totalprice": 250,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2026-07-20",
                        "checkout": "2026-07-24",
                    },
                    "additionalneeds": "API portfolio demo",
                },
            },
        )

    return httpx.Response(404, json={"error": "not found"})
