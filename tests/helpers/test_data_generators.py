import pytest

from utils.helpers.data import (
    booking_payload,
    random_email,
    random_phone,
    random_string,
    random_username,
    timestamped_value,
    unique_id,
)

pytestmark = pytest.mark.helpers


def test_unique_id_uses_prefix():
    assert unique_id("case").startswith("case-")


def test_random_email_uses_domain():
    assert random_email("example.test").endswith("@example.test")


def test_random_string_length():
    assert len(random_string(12)) == 12


def test_booking_payload_contains_required_contract_fields():
    payload = booking_payload()

    assert payload["firstname"] == "API"
    assert payload["bookingdates"]["checkout"] > payload["bookingdates"]["checkin"]


def test_web_style_data_helpers_generate_readable_values():
    assert timestamped_value("run").startswith("run-")
    assert random_username("qa").startswith("qa_")
    assert random_phone("+962", 9).startswith("+962")
