"""Example REST service layer."""

from __future__ import annotations

from typing import Any

import httpx

from clients import ApiClient


class BookingService:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def health(self) -> httpx.Response:
        return self.client.get("/health", expected_status=200)

    def create_booking(self, payload: dict[str, Any]) -> httpx.Response:
        return self.client.post("/bookings", json_body=payload, expected_status=201)

    def get_booking(self, booking_id: int) -> httpx.Response:
        return self.client.get(f"/bookings/{booking_id}", expected_status=200)
