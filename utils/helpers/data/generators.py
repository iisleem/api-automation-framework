"""Small deterministic-friendly data generators."""

from __future__ import annotations

import random
import string
import uuid
from datetime import date, datetime, timedelta, timezone


def unique_id(prefix: str = "api") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def timestamped_value(prefix: str = "api") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}-{timestamp}"


def random_string(length: int = 8, alphabet: str = string.ascii_lowercase) -> str:
    return "".join(random.choice(alphabet) for _ in range(length))


def random_email(domain: str = "example.test", prefix: str = "automation") -> str:
    return f"{prefix}.{uuid.uuid4().hex[:10]}@{domain}"


def random_username(prefix: str = "user", length: int = 8) -> str:
    suffix = random_string(length, string.ascii_lowercase + string.digits)
    return f"{prefix}_{suffix}"


def random_phone(country_code: str = "+1", digits: int = 10) -> str:
    number = "".join(random.choices(string.digits, k=digits))
    return f"{country_code}{number}"


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
