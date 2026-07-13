import json

import httpx
import pytest

from clients import ApiClient
from services import BookingService
from utils.helpers.data import booking_payload as build_booking_payload

pytestmark = [pytest.mark.smoke, pytest.mark.rest]


def test_rest_client_get_health_matches_schema(schema_validator):
    client = ApiClient("https://mock.api.local", transport=httpx.MockTransport(_rest_handler))
    service = BookingService(client)

    response = service.health()

    assert response.status_code == 200
    schema_validator.assert_matches_schema(response.json(), "schemas/rest/health.schema.json")
    client.close()


def test_rest_client_create_booking_matches_schema(schema_validator):
    client = ApiClient("https://mock.api.local", transport=httpx.MockTransport(_rest_handler))
    service = BookingService(client)

    response = service.create_booking(build_booking_payload("Portfolio", "API"))

    assert response.status_code == 201
    assert response.json()["booking"]["firstname"] == "Portfolio"
    schema_validator.assert_matches_schema(response.json(), "schemas/rest/booking.schema.json")
    client.close()


def _rest_handler(request: httpx.Request) -> httpx.Response:
    if request.method == "GET" and request.url.path == "/health":
        return httpx.Response(
            200,
            json={
                "status": "ok",
                "service": "booking-api",
                "timestamp": "2026-07-13T09:00:00Z",
            },
            headers={"content-type": "application/json"},
        )

    if request.method == "POST" and request.url.path == "/bookings":
        payload = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            201,
            json={
                "bookingid": 101,
                "booking": payload,
            },
            headers={"content-type": "application/json"},
        )

    return httpx.Response(404, json={"error": "not found"})
