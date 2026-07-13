"""Small deterministic-friendly data generators."""

from __future__ import annotations

import random
from datetime import date, timedelta

from automation_core.helpers.data import (
    random_email,
    random_phone,
    random_string,
    random_username,
    timestamped_value,
    unique_id,
)


def booking_payload(firstname: str = "API", lastname: str = "Tester") -> dict:
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=2)
    return {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": random.randint(100, 500),
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        },
        "additionalneeds": "Generated test data",
    }


__all__ = [
    "booking_payload",
    "random_email",
    "random_phone",
    "random_string",
    "random_username",
    "timestamped_value",
    "unique_id",
]
